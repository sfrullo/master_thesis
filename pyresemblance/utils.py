import logging
import numpy as np

def edge_mirror_3(x, width=((3,), (3,), (3,))):
    # y = cat(2, x(:, width(2)+1:-1:2,:), x, x(: ,end-1:-1:end-width(2),:));
    # y = cat(1, y(width(1)+1:-1:2, :,:), y, y(end-1:-1:end-width(1), :,:));
    # z = cat(3, y(:,:,width(3)+1:-1:2), y, y(:,:,end-1:-1:end-width(3)));
    result = np.lib.pad(x, width, 'reflect')
    logging.info(result)
    return result