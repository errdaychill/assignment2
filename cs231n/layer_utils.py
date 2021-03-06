from cs231n.layers import *
from cs231n.fast_layers import *


def affine_relu_forward(x, w, b):
    """
    Convenience layer that perorms an affine transform followed by a ReLU

    Inputs:
    - x: Input to the affine layer
    - w, b: Weights for the affine layer

    Returns a tuple of:
    - out: Output from the ReLU
    - cache: Object to give to the backward pass
    """
    a, fc_cache = affine_forward(x, w, b)
    out, relu_cache = relu_forward(a)
    cache = (fc_cache, relu_cache)
    return out, cache


def affine_relu_backward(dout, cache):
    """
    Backward pass for the affine-relu convenience layer
    """
    fc_cache, relu_cache = cache
    da = relu_backward(dout, relu_cache)
    dx, dw, db = affine_backward(da, fc_cache)
    return dx, dw, db

def affine_bn_relu_forward(x,w,b,gamma,beta,bn_param):
    out1, cache1 = affine_forward(x,w,b)      #cache1 = x, w, b
    out2, cache2 = batchnorm_forward(out1,gamma,beta,bn_param) #cache2 = out1, mu, var, std, xhat, gamma, beta
    out3, cache3 = relu_forward(out2) # cache3 = out2
    cache = (cache1, cache2, cache3)
    return out3, cache
    
def affine_bn_relu_backward(dout,cache):
    affine_cache, bn_cache, relu_cache = cache
    dinput3 = relu_backward(dout,relu_cache) #cache = input3
    dinput2, dgamma, dbeta = batchnorm_backward(dinput3,bn_cache) #cache = input2, gamma, beta
    dinput1, dw, db = affine_backward(dinput2, affine_cache)# cache = input1, w, b
    return dinput1, dw, db, dgamma, dbeta

def affine_ln_relu_forward(x,w,b,gamma,beta,bn_param):
    out1, cache1 = affine_forward(x,w,b)      #cache1 = x, w, b
    out2, cache2 = layernorm_forward(out1,gamma,beta,bn_param) #cache2 = out1, mu, var, std, xhat, gamma, beta
    out3, cache3 = relu_forward(out2) # cache3 = out2
    cache = (cache1,cache2,cache3)
    return out3, cache

def affine_ln_relu_backward(dout,cache):
    affine_cache, bn_cache, relu_cache = cache
    dinput3 = relu_backward(dout,relu_cache) #cache = input3
    dinput2, dgamma, dbeta = layernorm_backward(dinput3,bn_cache) #cache = input2, gamma, beta
    dinput1, dw, db = affine_backward(dinput2, affine_cache)# cache = input1, w, b
    return dinput1, dw, db, dgamma, dbeta    

def conv_relu_forward(x, w, b, conv_param):
    """
    A convenience layer that performs a convolution followed by a ReLU.

    Inputs:
    - x: Input to the convolutional layer
    - w, b, conv_param: Weights and parameters for the convolutional layer

    Returns a tuple of:
    - out: Output from the ReLU
    - cache: Object to give to the backward pass
    """
    a, conv_cache = conv_forward_fast(x, w, b, conv_param)
    out, relu_cache = relu_forward(a)
    cache = (conv_cache, relu_cache)
    return out, cache


def conv_relu_backward(dout, cache):
    """
    Backward pass for the conv-relu convenience layer.
    """
    conv_cache, relu_cache = cache
    da = relu_backward(dout, relu_cache)
    dx, dw, db = conv_backward_fast(da, conv_cache)
    return dx, dw, db


def conv_bn_relu_forward(x, w, b, gamma, beta, conv_param, bn_param):
    a, conv_cache = conv_forward_fast(x, w, b, conv_param)
    an, bn_cache = spatial_batchnorm_forward(a, gamma, beta, bn_param)
    out, relu_cache = relu_forward(an)
    cache = (conv_cache, bn_cache, relu_cache)
    return out, cache


def conv_bn_relu_backward(dout, cache):
    conv_cache, bn_cache, relu_cache = cache
    dan = relu_backward(dout, relu_cache)
    da, dgamma, dbeta = spatial_batchnorm_backward(dan, bn_cache)
    dx, dw, db = conv_backward_fast(da, conv_cache)
    return dx, dw, db, dgamma, dbeta


def conv_relu_pool_forward(x, w, b, conv_param, pool_param):
    """
    Convenience layer that performs a convolution, a ReLU, and a pool.

    Inputs:
    - x: Input to the convolutional layer
    - w, b, conv_param: Weights and parameters for the convolutional layer
    - pool_param: Parameters for the pooling layer

    Returns a tuple of:
    - out: Output from the pooling layer
    - cache: Object to give to the backward pass
    """
    a, conv_cache = conv_forward_fast(x, w, b, conv_param)
    s, relu_cache = relu_forward(a)
    out, pool_cache = max_pool_forward_fast(s, pool_param)
    cache = (conv_cache, relu_cache, pool_cache)
    return out, cache


def conv_relu_pool_backward(dout, cache):
    """
    Backward pass for the conv-relu-pool convenience layer
    """
    conv_cache, relu_cache, pool_cache = cache
    ds = max_pool_backward_fast(dout, pool_cache)
    da = relu_backward(ds, relu_cache)
    dx, dw, db = conv_backward_fast(da, conv_cache)
    return dx, dw, db
