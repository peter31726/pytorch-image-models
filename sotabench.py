import torch
from torchbench.image_classification import ImageNet
from timm import create_model
from timm.data import resolve_data_config, create_transform
from timm.models import TestTimePoolHead
import os

NUM_GPU = 1
BATCH_SIZE = 256 * NUM_GPU


def _entry(model_name, paper_model_name, paper_arxiv_id, batch_size=BATCH_SIZE,
           ttp=False, args=dict(), model_desc=None):
    return dict(
        model=model_name,
        model_description=model_desc,
        paper_model_name=paper_model_name,
        paper_arxiv_id=paper_arxiv_id,
        batch_size=batch_size,
        ttp=ttp,
        args=args)

# NOTE For any original PyTorch models, I'll remove from this list when you add to sotabench to
# avoid overlap and confusion. Please contact me.
model_list = [
    ## Weights ported by myself from other frameworks or trained myself in PyTorch
    _entry('adv_inception_v3', 'Adversarial Inception V3', '1611.01236',
           model_desc='Ported from official Tensorflow weights'),
    _entry('ens_adv_inception_resnet_v2', 'Ensemble Adversarial Inception V3', '1705.07204',
           model_desc='Ported from official Tensorflow weights'),
    _entry('dpn68', 'DPN-68 (224x224)', '1707.01629'),
    _entry('dpn68b', 'DPN-68b (224x224)', '1707.01629'),
    _entry('dpn92', 'DPN-92 (224x224)', '1707.01629'),
    _entry('dpn98', 'DPN-98 (224x224)', '1707.01629'),
    _entry('dpn107', 'DPN-107 (224x224)', '1707.01629'),
    _entry('dpn131', 'DPN-131 (224x224)', '1707.01629'),
    _entry('dpn68', 'DPN-68 (320x320, Mean-Max Pooling)', '1707.01629', ttp=True, args=dict(img_size=320)),
    _entry('dpn68b', 'DPN-68b (320x320, Mean-Max Pooling)', '1707.01629', ttp=True, args=dict(img_size=320)),
    _entry('dpn92', 'DPN-92 (320x320, Mean-Max Pooling)', '1707.01629',
           ttp=True, args=dict(img_size=320), batch_size=BATCH_SIZE//2),
    _entry('dpn98', 'DPN-98 (320x320, Mean-Max Pooling)', '1707.01629',
           ttp=True, args=dict(img_size=320), batch_size=BATCH_SIZE//2),
    _entry('dpn107', 'DPN-107 (320x320, Mean-Max Pooling)', '1707.01629',
           ttp=True, args=dict(img_size=320), batch_size=BATCH_SIZE//4),
    _entry('dpn131', 'DPN-131 (320x320, Mean-Max Pooling)', '1707.01629',
           ttp=True, args=dict(img_size=320), batch_size=BATCH_SIZE//4),
    _entry('efficientnet_b0', 'EfficientNet-B0', '1905.11946'),
    _entry('efficientnet_b1', 'EfficientNet-B1', '1905.11946'),
    _entry('efficientnet_b2', 'EfficientNet-B2', '1905.11946',
           model_desc='Trained from scratch in PyTorch w/ RandAugment'),
    _entry('efficientnet_b2a', 'EfficientNet-B2 (288x288, 1.0 crop)', '1905.11946',
           model_desc='Trained from scratch in PyTorch w/ RandAugment'),
    _entry('efficientnet_b3', 'EfficientNet-B3', '1905.11946',
           model_desc='Trained from scratch in PyTorch w/ RandAugment'),
    _entry('efficientnet_b3a', 'EfficientNet-B3 (320x320, 1.0 crop)', '1905.11946',
           model_desc='Trained from scratch in PyTorch w/ RandAugment'),
    _entry('fbnetc_100', 'FBNet-C', '1812.03443',
           model_desc='Trained in PyTorch with RMSProp, exponential LR decay'),
    _entry('gluon_inception_v3', 'Inception V3', '1512.00567', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnet18_v1b', 'ResNet-18', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnet34_v1b', 'ResNet-34', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnet50_v1b', 'ResNet-50', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnet50_v1c', 'ResNet-50-C', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnet50_v1d', 'ResNet-50-D', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnet50_v1s', 'ResNet-50-S', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnet101_v1b', 'ResNet-101', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnet101_v1c', 'ResNet-101-C', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnet101_v1d', 'ResNet-101-D', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnet101_v1s', 'ResNet-101-S', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnet152_v1b', 'ResNet-152', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnet152_v1c', 'ResNet-152-C', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnet152_v1d', 'ResNet-152-D', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnet152_v1s', 'ResNet-152-S', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnext50_32x4d', 'ResNeXt-50 32x4d', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnext101_32x4d', 'ResNeXt-101 32x4d', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_resnext101_64x4d', 'ResNeXt-101 64x4d', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_senet154', 'SENet-154', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_seresnext50_32x4d', 'SE-ResNeXt-50 32x4d', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_seresnext101_32x4d', 'SE-ResNeXt-101 32x4d', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_seresnext101_64x4d', 'SE-ResNeXt-101 64x4d', '1812.01187', model_desc='Ported from GluonCV Model Zoo'),
    _entry('gluon_xception65', 'Modified Aligned Xception', '1802.02611', batch_size=BATCH_SIZE//2,
           model_desc='Ported from GluonCV Model Zoo'),
    _entry('mixnet_xl', 'MixNet-XL', '1907.09595', model_desc="My own scaling beyond paper's MixNet Large"),
    _entry('mixnet_l', 'MixNet-L', '1907.09595'),
    _entry('mixnet_m', 'MixNet-M', '1907.09595'),
    _entry('mixnet_s', 'MixNet-S', '1907.09595'),
    _entry('mnasnet_100', 'MnasNet-B1', '1807.11626'),
    _entry('mobilenetv3_rw', 'MobileNet V3-Large 1.0', '1905.02244',
           model_desc='Trained in PyTorch with RMSProp, exponential LR decay, and hyper-params matching '
                      'paper as closely as possible.'),
    _entry('resnet18', 'ResNet-18', '1812.01187'),
    _entry('resnet26', 'ResNet-26', '1812.01187', model_desc='Block cfg of ResNet-34 w/ Bottleneck'),
    _entry('resnet26d', 'ResNet-26-D', '1812.01187',
           model_desc='Block cfg of ResNet-34 w/ Bottleneck, deep stem, and avg-pool in downsample layers.'),
    _entry('resnet34', 'ResNet-34', '1812.01187'),
    _entry('resnet50', 'ResNet-50', '1812.01187', model_desc='Trained with AugMix + JSD loss'),
    _entry('resnet50', 'ResNet-50 (288x288 Mean-Max Pooling)', '1812.01187',
           ttp=True, args=dict(img_size=288),
           model_desc='Trained with AugMix + JSD loss'),
    _entry('resnext50_32x4d', 'ResNeXt-50 32x4d', '1812.01187'),
    _entry('resnext50d_32x4d', 'ResNeXt-50-D 32x4d', '1812.01187',
           model_desc="'D' variant (3x3 deep stem w/ avg-pool downscale). Trained with "
                      "SGD w/ cosine LR decay, random-erasing (gaussian per-pixel noise) and label-smoothing"),
    _entry('semnasnet_100', 'MnasNet-A1', '1807.11626'),
    _entry('seresnet18', 'SE-ResNet-18', '1709.01507'),
    _entry('seresnet34', 'SE-ResNet-34', '1709.01507'),
    _entry('seresnext26_32x4d', 'SE-ResNeXt-26 32x4d', '1709.01507',
           model_desc='Block cfg of SE-ResNeXt-34 w/ Bottleneck'),
    _entry('seresnext26d_32x4d', 'SE-ResNeXt-26-D 32x4d', '1812.01187',
           model_desc='Block cfg of SE-ResNeXt-34 w/ Bottleneck, deep stem, and avg-pool in downsample layers.'),
    _entry('seresnext26t_32x4d', 'SE-ResNeXt-26-T 32x4d', '1812.01187',
           model_desc='Block cfg of SE-ResNeXt-34 w/ Bottleneck, deep tiered stem, and avg-pool in downsample layers.'),
    _entry('seresnext26tn_32x4d', 'SE-ResNeXt-26-TN 32x4d', '1812.01187',
           model_desc='Block cfg of SE-ResNeXt-34 w/ Bottleneck, deep tiered narrow stem, and avg-pool in downsample layers.'),
    _entry('spnasnet_100', 'Single-Path NAS', '1904.02877',
           model_desc='Trained in PyTorch with SGD, cosine LR decay'),
    _entry('tf_efficientnet_b0', 'EfficientNet-B0 (AutoAugment)', '1905.11946',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b1', 'EfficientNet-B1 (AutoAugment)', '1905.11946',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b2', 'EfficientNet-B2 (AutoAugment)', '1905.11946',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b3', 'EfficientNet-B3 (AutoAugment)', '1905.11946', batch_size=BATCH_SIZE//2,
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b4', 'EfficientNet-B4 (AutoAugment)', '1905.11946', batch_size=BATCH_SIZE//2,
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b5', 'EfficientNet-B5 (RandAugment)', '1905.11946', batch_size=BATCH_SIZE//4,
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b6', 'EfficientNet-B6 (AutoAugment)', '1905.11946', batch_size=BATCH_SIZE//8,
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b7', 'EfficientNet-B7 (RandAugment)', '1905.11946', batch_size=BATCH_SIZE//8,
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b0_ap', 'EfficientNet-B0 (AdvProp)', '1911.09665',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b1_ap', 'EfficientNet-B1 (AdvProp)', '1911.09665',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b2_ap', 'EfficientNet-B2 (AdvProp)', '1911.09665',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b3_ap', 'EfficientNet-B3 (AdvProp)', '1911.09665', batch_size=BATCH_SIZE // 2,
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b4_ap', 'EfficientNet-B4 (AdvProp)', '1911.09665', batch_size=BATCH_SIZE // 2,
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b5_ap', 'EfficientNet-B5 (AdvProp)', '1911.09665', batch_size=BATCH_SIZE // 4,
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b6_ap', 'EfficientNet-B6 (AdvProp)', '1911.09665', batch_size=BATCH_SIZE // 8,
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b7_ap', 'EfficientNet-B7 (AdvProp)', '1911.09665', batch_size=BATCH_SIZE // 8,
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_b8_ap', 'EfficientNet-B8 (AdvProp)', '1911.09665', batch_size=BATCH_SIZE // 8,
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_cc_b0_4e', 'EfficientNet-CondConv-B0 4 experts', '1904.04971',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_cc_b0_8e', 'EfficientNet-CondConv-B0 8 experts', '1904.04971',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_cc_b1_8e', 'EfficientNet-CondConv-B1 8 experts', '1904.04971',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_es', 'EfficientNet-EdgeTPU-S', '1905.11946',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_em', 'EfficientNet-EdgeTPU-M', '1905.11946',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_efficientnet_el', 'EfficientNet-EdgeTPU-L', '1905.11946', batch_size=BATCH_SIZE//2,
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_inception_v3', 'Inception V3', '1512.00567', model_desc='Ported from official Tensorflow weights'),
    _entry('tf_mixnet_l', 'MixNet-L', '1907.09595', model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_mixnet_m', 'MixNet-M', '1907.09595', model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_mixnet_s', 'MixNet-S', '1907.09595', model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_mobilenetv3_large_100', 'MobileNet V3-Large 1.0', '1905.02244',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_mobilenetv3_large_075', 'MobileNet V3-Large 0.75', '1905.02244',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_mobilenetv3_large_minimal_100', 'MobileNet V3-Large Minimal 1.0', '1905.02244',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_mobilenetv3_small_100', 'MobileNet V3-Small 1.0', '1905.02244',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_mobilenetv3_small_075', 'MobileNet V3-Small 0.75', '1905.02244',
           model_desc='Ported from official Google AI Tensorflow weights'),
    _entry('tf_mobilenetv3_small_minimal_100', 'MobileNet V3-Small Minimal 1.0', '1905.02244',
           model_desc='Ported from official Google AI Tensorflow weights'),

    ## Cadene ported weights (to remove if Cadene adds sotabench)
    _entry('inception_resnet_v2', 'Inception ResNet V2', '1602.07261'),
    _entry('inception_v4', 'Inception V4', '1602.07261'),
    _entry('nasnetalarge', 'NASNet-A Large', '1707.07012', batch_size=BATCH_SIZE // 4),
    _entry('pnasnet5large', 'PNASNet-5', '1712.00559', batch_size=BATCH_SIZE // 4),
    _entry('seresnet50', 'SE-ResNet-50', '1709.01507'),
    _entry('seresnet101', 'SE-ResNet-101', '1709.01507'),
    _entry('seresnet152', 'SE-ResNet-152', '1709.01507'),
    _entry('seresnext50_32x4d', 'SE-ResNeXt-50 32x4d', '1709.01507'),
    _entry('seresnext101_32x4d', 'SE-ResNeXt-101 32x4d', '1709.01507'),
    _entry('senet154', 'SENet-154', '1709.01507'),
    _entry('xception', 'Xception', '1610.02357',  batch_size=BATCH_SIZE//2),

    ## Torchvision weights
    # _entry('densenet121'),
    # _entry('densenet161'),
    # _entry('densenet169'),
    # _entry('densenet201'),
    # _entry('inception_v3', paper_model_name='Inception V3', ),
    # _entry('tv_resnet34', , ),
    # _entry('tv_resnet50', , ),
    # _entry('resnet101', , ),
    # _entry('resnet152', , ),
    # _entry('tv_resnext50_32x4d', , ),
    # _entry('resnext101_32x8d', ),
    # _entry('wide_resnet50_2' , ),
    # _entry('wide_resnet101_2', , ),

    ## Facebook WSL weights
    _entry('ig_resnext101_32x8d', 'ResNeXt-101 32x8d', '1805.00932',
           model_desc='Weakly-Supervised pre-training on 1B Instagram hashtag dataset by Facebook Research'),
    _entry('ig_resnext101_32x16d', 'ResNeXt-101 32x16d', '1805.00932',
           model_desc='Weakly-Supervised pre-training on 1B Instagram hashtag dataset by Facebook Research'),
    _entry('ig_resnext101_32x32d', 'ResNeXt-101 32x32d', '1805.00932', batch_size=BATCH_SIZE // 2,
           model_desc='Weakly-Supervised pre-training on 1B Instagram hashtag dataset by Facebook Research'),
    _entry('ig_resnext101_32x48d', 'ResNeXt-101 32x48d', '1805.00932', batch_size=BATCH_SIZE // 4,
           model_desc='Weakly-Supervised pre-training on 1B Instagram hashtag dataset by Facebook Research'),

    _entry('ig_resnext101_32x8d', 'ResNeXt-101 32x8d (288x288 Mean-Max Pooling)', '1805.00932',
           ttp=True, args=dict(img_size=288),
           model_desc='Weakly-Supervised pre-training on 1B Instagram hashtag dataset by Facebook Research'),
    _entry('ig_resnext101_32x16d', 'ResNeXt-101 32x16d (288x288 Mean-Max Pooling)', '1805.00932',
           ttp=True, args=dict(img_size=288), batch_size=BATCH_SIZE // 2,
           model_desc='Weakly-Supervised pre-training on 1B Instagram hashtag dataset by Facebook Research'),
    _entry('ig_resnext101_32x32d', 'ResNeXt-101 32x32d (288x288 Mean-Max Pooling)', '1805.00932',
           ttp=True, args=dict(img_size=288), batch_size=BATCH_SIZE // 4,
           model_desc='Weakly-Supervised pre-training on 1B Instagram hashtag dataset by Facebook Research'),
    _entry('ig_resnext101_32x48d', 'ResNeXt-101 32x48d (288x288 Mean-Max Pooling)', '1805.00932',
           ttp=True, args=dict(img_size=288), batch_size=BATCH_SIZE // 8,
           model_desc='Weakly-Supervised pre-training on 1B Instagram hashtag dataset by Facebook Research'),

    ## Facebook SSL weights
    _entry('ssl_resnet18', 'ResNet-18', '1905.00546',
           model_desc='Semi-Supervised pre-training on YFCC100M dataset by Facebook Research'),
    _entry('ssl_resnet50', 'ResNet-50', '1905.00546',
           model_desc='Semi-Supervised pre-training on YFCC100M dataset by Facebook Research'),
    _entry('ssl_resnext50_32x4d', 'ResNeXt-50 32x4d', '1905.00546',
           model_desc='Semi-Supervised pre-training on YFCC100M dataset by Facebook Research'),
    _entry('ssl_resnext101_32x4d', 'ResNeXt-101 32x4d', '1905.00546',
           model_desc='Semi-Supervised pre-training on YFCC100M dataset by Facebook Research'),
    _entry('ssl_resnext101_32x8d', 'ResNeXt-101 32x8d', '1905.00546',
           model_desc='Semi-Supervised pre-training on YFCC100M dataset by Facebook Research'),
    _entry('ssl_resnext101_32x16d', 'ResNeXt-101 32x16d', '1905.00546',
           model_desc='Semi-Supervised pre-training on YFCC100M dataset by Facebook Research'),

    _entry('ssl_resnet50', 'ResNet-50 (288x288 Mean-Max Pooling)', '1905.00546',
           ttp=True, args=dict(img_size=288),
           model_desc='Semi-Supervised pre-training on YFCC100M dataset by Facebook Research'),
    _entry('ssl_resnext50_32x4d', 'ResNeXt-50 32x4d (288x288 Mean-Max Pooling)', '1905.00546',
           ttp=True, args=dict(img_size=288),
           model_desc='Semi-Supervised pre-training on YFCC100M dataset by Facebook Research'),
    _entry('ssl_resnext101_32x4d', 'ResNeXt-101 32x4d (288x288 Mean-Max Pooling)', '1905.00546',
           ttp=True, args=dict(img_size=288),
           model_desc='Semi-Supervised pre-training on YFCC100M dataset by Facebook Research'),
    _entry('ssl_resnext101_32x8d', 'ResNeXt-101 32x8d (288x288 Mean-Max Pooling)', '1905.00546',
           ttp=True, args=dict(img_size=288),
           model_desc='Semi-Supervised pre-training on YFCC100M dataset by Facebook Research'),
    _entry('ssl_resnext101_32x16d', 'ResNeXt-101 32x16d (288x288 Mean-Max Pooling)', '1905.00546',
           ttp=True, args=dict(img_size=288), batch_size=BATCH_SIZE // 2,
           model_desc='Semi-Supervised pre-training on YFCC100M dataset by Facebook Research'),

    ## Facebook SWSL weights
    _entry('swsl_resnet18', 'ResNet-18', '1905.00546',
           model_desc='Semi-Weakly-Supervised pre-training on 1 billion unlabelled dataset by Facebook Research'),
    _entry('swsl_resnet50', 'ResNet-50', '1905.00546',
           model_desc='Semi-Weakly-Supervised pre-training on 1 billion unlabelled dataset by Facebook Research'),
    _entry('swsl_resnext50_32x4d', 'ResNeXt-50 32x4d', '1905.00546',
           model_desc='Semi-Weakly-Supervised pre-training on 1 billion unlabelled dataset by Facebook Research'),
    _entry('swsl_resnext101_32x4d', 'ResNeXt-101 32x4d', '1905.00546',
           model_desc='Semi-Weakly-Supervised pre-training on 1 billion unlabelled dataset by Facebook Research'),
    _entry('swsl_resnext101_32x8d', 'ResNeXt-101 32x8d', '1905.00546',
           model_desc='Semi-Weakly-Supervised pre-training on 1 billion unlabelled dataset by Facebook Research'),
    _entry('swsl_resnext101_32x16d', 'ResNeXt-101 32x16d', '1905.00546',
           model_desc='Semi-Weakly-Supervised pre-training on 1 billion unlabelled dataset by Facebook Research'),

    _entry('swsl_resnet50', 'ResNet-50 (288x288 Mean-Max Pooling)', '1905.00546',
           ttp=True, args=dict(img_size=288),
           model_desc='Semi-Weakly-Supervised pre-training on 1 billion unlabelled dataset by Facebook Research'),
    _entry('swsl_resnext50_32x4d', 'ResNeXt-50 32x4d (288x288 Mean-Max Pooling)', '1905.00546',
           ttp=True, args=dict(img_size=288),
           model_desc='Semi-Weakly-Supervised pre-training on 1 billion unlabelled dataset by Facebook Research'),
    _entry('swsl_resnext101_32x4d', 'ResNeXt-101 32x4d (288x288 Mean-Max Pooling)', '1905.00546',
           ttp=True, args=dict(img_size=288),
           model_desc='Semi-Weakly-Supervised pre-training on 1 billion unlabelled dataset by Facebook Research'),
    _entry('swsl_resnext101_32x8d', 'ResNeXt-101 32x8d (288x288 Mean-Max Pooling)', '1905.00546',
           ttp=True, args=dict(img_size=288),
           model_desc='Semi-Weakly-Supervised pre-training on 1 billion unlabelled dataset by Facebook Research'),
    _entry('swsl_resnext101_32x16d', 'ResNeXt-101 32x16d (288x288 Mean-Max Pooling)', '1905.00546',
           ttp=True, args=dict(img_size=288), batch_size=BATCH_SIZE // 2,
           model_desc='Semi-Weakly-Supervised pre-training on 1 billion unlabelled dataset by Facebook Research'),

    ## DLA official impl weights (to remove if sotabench added to source)
    _entry('dla34', 'DLA-34', '1707.06484'),
    _entry('dla46_c', 'DLA-46-C', '1707.06484'),
    _entry('dla46x_c', 'DLA-X-46-C', '1707.06484'),
    _entry('dla60x_c', 'DLA-X-60-C', '1707.06484'),
    _entry('dla60', 'DLA-60', '1707.06484'),
    _entry('dla60x', 'DLA-X-60', '1707.06484'),
    _entry('dla102', 'DLA-102', '1707.06484'),
    _entry('dla102x', 'DLA-X-102', '1707.06484'),
    _entry('dla102x2', 'DLA-X-102 64', '1707.06484'),
    _entry('dla169', 'DLA-169', '1707.06484'),

    ## Res2Net official impl weights (to remove if sotabench added to source)
    _entry('res2net50_26w_4s', 'Res2Net-50 26x4s', '1904.01169'),
    _entry('res2net50_14w_8s', 'Res2Net-50 14x8s', '1904.01169'),
    _entry('res2net50_26w_6s', 'Res2Net-50 26x6s', '1904.01169'),
    _entry('res2net50_26w_8s', 'Res2Net-50 26x8s', '1904.01169'),
    _entry('res2net50_48w_2s', 'Res2Net-50 48x2s', '1904.01169'),
    _entry('res2net101_26w_4s', 'Res2NeXt-101 26x4s', '1904.01169'),
    _entry('res2next50', 'Res2NeXt-50', '1904.01169'),
    _entry('dla60_res2net', 'Res2Net-DLA-60', '1904.01169'),
    _entry('dla60_res2next', 'Res2NeXt-DLA-60', '1904.01169'),

    ## HRNet official impl weights
    _entry('hrnet_w18_small', 'HRNet-W18-C-Small-V1', '1908.07919'),
    _entry('hrnet_w18_small_v2', 'HRNet-W18-C-Small-V2', '1908.07919'),
    _entry('hrnet_w18', 'HRNet-W18-C', '1908.07919'),
    _entry('hrnet_w30', 'HRNet-W30-C', '1908.07919'),
    _entry('hrnet_w32', 'HRNet-W32-C', '1908.07919'),
    _entry('hrnet_w40', 'HRNet-W40-C', '1908.07919'),
    _entry('hrnet_w44', 'HRNet-W44-C', '1908.07919'),
    _entry('hrnet_w48', 'HRNet-W48-C', '1908.07919'),
    _entry('hrnet_w64', 'HRNet-W64-C', '1908.07919'),


    ## SelecSLS official impl weights
    _entry('selecsls42b', 'SelecSLS-42_B', '1907.00837',
           model_desc='Originally from https://github.com/mehtadushy/SelecSLS-Pytorch'),
    _entry('selecsls60', 'SelecSLS-60', '1907.00837',
           model_desc='Originally from https://github.com/mehtadushy/SelecSLS-Pytorch'),
    _entry('selecsls60b', 'SelecSLS-60_B', '1907.00837',
           model_desc='Originally from https://github.com/mehtadushy/SelecSLS-Pytorch'),
]

for m in model_list:
    model_name = m['model']
    # create model from name
    model = create_model(model_name, pretrained=True)
    param_count = sum([m.numel() for m in model.parameters()])
    print('Model %s, %s created. Param count: %d' % (model_name, m['paper_model_name'], param_count))

    # get appropriate transform for model's default pretrained config
    data_config = resolve_data_config(m['args'], model=model, verbose=True)
    if m['ttp']:
        model = TestTimePoolHead(model, model.default_cfg['pool_size'])
        data_config['crop_pct'] = 1.0
    input_transform = create_transform(**data_config)

    # Run the benchmark
    ImageNet.benchmark(
        model=model,
        model_description=m.get('model_description', None),
        paper_model_name=m['paper_model_name'],
        paper_arxiv_id=m['paper_arxiv_id'],
        input_transform=input_transform,
        batch_size=m['batch_size'],
        num_gpu=NUM_GPU,
        data_root=os.environ.get('IMAGENET_DIR', './imagenet')
    )

    torch.cuda.empty_cache()


