
import torch
import torch.utils.data as data
import os
import numpy as np


class PrecompDataset(data.Dataset):
    """
    Load precomputed captions and image features
    Possible options: f30k_precomp, coco_precomp
    """
    def __init__(self, data_path, data_split):
        loc = data_path + '/'
        self.data_split = data_split

        self.captions = []
        file_name = loc + '%s_caps.txt' % data_split
        if os.path.exists(file_name):
            with open(file_name, 'rb') as f:
                for line in f:
                    self.captions.append(line.strip())
        print('path:'+loc+data_split)
        if self.data_split.startswith("train"):
            self.length = len(self.captions)
            self.images = np.load(loc + data_split +'_ims.npy')
            
            print(data_split +'length')
            print(len(self.images))
        else:
            self.length = len(self.captions)

            self.images = np.load(loc + data_split + '_ims.npy')
            self.images = self.images[::5,:,:]
            # 
        print('load '+ data_split +'_image done')



        if data_split.startswith("train"):
            value = np.load(loc + data_split + '_captions.npz',allow_pickle=True)
            self.captions = value['arr_0']
            print('after bert, the length of caption:')
            print(len(self.captions))
            print('load ' + data_split + '_caption done')
        
        else:
            self.captions = np.load(loc + data_split + '_captions.npy',allow_pickle=True)
            print('load ' + data_split + '_caption done')


        print("Len in captions in {0} is {1}".format(data_split,self.length))
        self.public_data = True

        self.im_div = 5
        if self._get_data_split(data_split):
            if len(self.captions) > len(self.images):
                self.length = len(self.captions)
                self.im_div = len(self.captions) / len(self.images)
            else:
                self.length = len(self.images)
                self.im_div = len(self.images) / len(self.captions)
                self.public_data = False

    def _get_data_split(self, data_split):
        if data_split.startswith("test"):
            return True
        return False

    def __getitem__(self, index):
        # handle the image redundancy
        img_id = int(index / self.im_div)
        cap_id = index
        if not self.public_data:
            img_id = index
            cap_id = index / self.im_div

        image = torch.Tensor(self.images[int(img_id)])
        target = torch.Tensor(self.captions[int(cap_id)])
                 
            
        return image, target, index, img_id

    def __len__(self):
        return self.length


def collate_fn(data):

    data.sort(key=lambda x: len(x[1]), reverse=True)
    images, captions, ids, img_ids = zip(*data)
    images = torch.stack(images, 0)



    # Merget captions (convert tuple of 1D tensor to 2D tensor)
    lengths = [cap.size(0) for cap in captions]
    targets = torch.zeros(len(captions), max(lengths), 768)
    for i, cap in enumerate(captions):
        for j, word_tensor in enumerate(cap):
            targets[i, j, :] = word_tensor

    return images, targets, lengths, ids


def get_precomp_loader(data_path, data_split, batch_size=100,
                       shuffle=True, num_workers=2):
    """Returns torch.utils.data.DataLoader for custom coco dataset."""
    dset = PrecompDataset(data_path, data_split)
    data_loader = torch.utils.data.DataLoader(dataset=dset,
                                              batch_size=batch_size,
                                              shuffle=shuffle,
                                              pin_memory=True,
                                              collate_fn=collate_fn)
    return data_loader


def get_loaders(data_name, batch_size, workers, opt):
    dpath = os.path.join(opt.data_path, data_name)
    train_loader = get_precomp_loader(dpath, 'train',  batch_size, True, workers)
    val_loader = get_precomp_loader(dpath, 'dev', batch_size, False, workers)
    return train_loader, val_loader


def get_test_loader(split_name, data_name, batch_size,
                    workers, opt):
    dpath = opt.data_path
    test_loader = get_precomp_loader(dpath, split_name, 
                                     batch_size, False, workers)
    return test_loader
