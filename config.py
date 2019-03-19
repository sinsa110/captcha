TRAIN_DIR = "./train_data"
VALID_DIR = "./valid_data"
TEST_DIR = "./test_data"
N_CLASS = 4
N_CHAR = "0123456789abcdefghijklmnopqrstuvwxyz"
CHAR_DICT = {k: i for i, k in enumerate(list(N_CHAR))}
LOSS = "categorical_crossentropy"
OPTIMIZER = "Adam"
METRICS = "accuracy"
IMAGES_H = 70
IMAGES_W = 160
CHANNEL = 3
KEEP_PROB = 0.5
FILTERS_1 = 64
FILTERS_2 = 64
FILTERS_3 = 64
FILTERS_4 = 64

EPOCH = 20
BATCH_SIZE = 256
PATIENCE = 10
