import os
import tensorflow as tf
import tensorflow_hub as hub

import utils

# Model initialization
utils.log('Loading pre-trained model...')

os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
nst_model = hub.load(handle)

# Run the pre-trained model
def stylize(content_img, style_img):
  stylized_image = nst_model(tf.constant(content_img), tf.constant(style_img))[0]
  return utils.tensor_to_pil_image(stylized_image)