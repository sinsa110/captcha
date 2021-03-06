# -*- coding: utf-8 -*-
import os
import keras.backend as K
from keras.models import Model, load_model
from keras.layers import Dense, Input, Conv2D, Reshape
from keras.layers import MaxPooling2D, Flatten, Dropout
from keras.callbacks import EarlyStopping, TensorBoard
from keras.utils import plot_model
import numpy as np
import matplotlib.pyplot as plt


class CaptchaCnn(object):

    def __init__(self):
        self.model = None
        self.images_w = None
        self.images_h = None
        self.channel = None
        self.n_class = None
        self.n_char = None
        self.loss = None
        self.optimizer = None
        self.metrics = None
        self.keep_prob = None
        self.path = "model/"
        self.logs = "logs/"
        self.model_file = "cnn_model"

    def __str__(self):
        return "The is my cnn!"

    def set_param(self, **kwargs):
        self.images_w = kwargs['images_w']
        self.images_h = kwargs['images_h']
        self.channel = kwargs['channel']
        self.n_class = kwargs['n_class']
        self.n_char = kwargs['n_char']
        self.loss = kwargs['loss']
        self.optimizer = kwargs['optimizer']
        self.metrics = kwargs['metrics']
        self.keep_prob = kwargs['keep_prob']

    def building_model(self, **kwargs):
        """

        :param kwargs: filters_1 第一层卷积数
                       filters_2 第二层卷积数
                       filters_3 第三层卷积数
                       filters_4 第四层卷积数
        :return: 模型对象
        """
        # 模型输入
        input_x = Input(shape=(self.images_h, self.images_w, self.channel), name="input_x")
        # 第一层卷积
        conv_1 = Conv2D(kwargs["filters_1"], kernel_size=[3, 3], activation="relu")(input_x)
        pooling_1 = MaxPooling2D((2, 2))(conv_1)
        # 第二层卷积
        conv_2 = Conv2D(kwargs["filters_2"], kernel_size=[3, 3], activation="relu")(pooling_1)
        pooling_2 = MaxPooling2D((2, 2))(conv_2)
        # 第三层卷积
        conv_3 = Conv2D(kwargs["filters_3"], kernel_size=[3, 3], activation="relu")(pooling_2)
        pooling_3 = MaxPooling2D((2, 2))(conv_3)
        # 第四层卷积
        conv_4 = Conv2D(kwargs["filters_4"], kernel_size=[3, 3], activation="relu")(pooling_3)
        pooling_4 = MaxPooling2D((2, 2))(conv_4)
        # 压平数据
        flatten = Flatten()(pooling_4)
        # dropout层
        dropout = Dropout(self.keep_prob)(flatten)
        # 分类输出
        output_1 = Dense(units=self.n_class * len(self.n_char), activation="softmax")(dropout)
        # 将输出转换为矩阵格式
        output_2 = Reshape((self.n_class, len(self.n_char)))(output_1)
        # 模型对象
        self.model = Model(inputs=input_x, outputs=output_2)
        try:
            self.model.compile(loss=self.loss, optimizer=self.optimizer, metrics=[self.metrics])
        except Exception as e:
            print("[building_model]" + str(e))

    def _model_summary(self):
        """

        :return: 模型结构
        """
        return self.model.summary()

    def fit_model(self, x_train, y_train, **kwargs):
        """

        :param x_train: 训练特征
        :param y_train: 训练标签
        :param kwargs: epochs: 迭代次数
                        batch_size: 批量训练数据大小
                        patience: 在损失函数无减少后多次迭代结束训练
        :return:
        """
        try:
            if self.model is None:
                raise Exception("Model is not be building!")
            else:
                self._model_summary()
                early_stop = EarlyStopping(patience=kwargs['patience'])
                if os.path.exists(self.logs) is False:
                    os.mkdir(self.logs)
                tensor_board = TensorBoard()
                try:
                    x_train_val = kwargs['x_train_val']
                    y_train_val = kwargs['y_train_val']
                    self.H = self.model.fit(x=x_train, y=y_train
                                            , epochs=kwargs.get('epochs', 10)
                                            , batch_size=kwargs.get('batch_size', 128)
                                            , validation_data=(x_train_val, y_train_val)
                                            , callbacks=[early_stop, tensor_board]
                                            )
                except:
                    self.H = self.model.fit(x=x_train, y=y_train
                                            , epochs=kwargs['epochs']
                                            , batch_size=kwargs['batch_size']
                                            , validation_split=0.1
                                            , callbacks=[early_stop, tensor_board]
                                            )
        except Exception as e:
            raise Exception("[fit_model]" + str(e))

    def model_save(self):
        """ 用于保存模型

        :return: None
        """
        try:
            if os.path.exists(self.path) is False:
                os.mkdir(self.path)
            self.model.save(self.path + self.model_file + ".h5")
            print("[INFO] Model is saved!")
        except Exception as e:
            print("[model_save]" + str(e))

    def model_load(self):
        """ 用于加载模型

        :return: None
        """
        try:
            self.model = load_model(self.path + self.model_file + ".h5")
            print("=" * 20)
            print("The model is loaded!")
            print("good luck!")
            print("=" * 20)
        except Exception as e:
            print("[model_load]" + str(e))

    def model_evaluation(self, x_test, y_test):
        """

        :param x_test: 评估特征
        :param y_test: 评估标签
        :return:
        """
        try:
            model_evaluate = self.model.evaluate(x_test, y_test)
            loss = model_evaluate[0]
            acc = model_evaluate[1]
            print("-" * 20)
            print("|loss: |", loss, " |")
            print("|acc: |", acc, " |")
            print("-" * 20)
        except Exception as e:
            print("[model_eval]" + str(e))

    def model_predict(self, x_data):
        """ 用于数据预测

        :param x_data: 预测数据
        :return:
        """
        try:
            return self.model.predict(x_data)
        except Exception as e:
            print("[model_predict]" + str(e))

    def plot_model(self):
        """ 模型可视化：保存模型结构为图片
        :return:
        """
        plot_model(self.model, to_file='model.png', show_shapes=True)

    def plot_loss_acc(self, **kwargs):
        """ 训练历史可视化：绘制训练集&验证集上的准确率值和损失值
        :param kwargs:
        :return:
        """
        N = np.arange(0, kwargs['epoch'])
        H = self.H

        plt.style.use("ggplot")
        plt.figure()

        plt.subplot(211)
        plt.title("Training Loss and Accuracy ")
        plt.plot(N, H.history["loss"], label="train_loss")
        plt.plot(N, H.history["val_loss"], label="val_loss")
        plt.ylabel("Loss")
        plt.legend()

        plt.subplot(212)
        plt.plot(N, H.history["acc"], label="train_acc")
        plt.plot(N, H.history["val_acc"], label="val_acc")
        plt.xlabel("Epoch #")
        plt.ylabel("Accuracy")
        plt.legend()
        fn = kwargs.get('file_name', '')
        plt.savefig(fn + "loss_acc.png")

    @staticmethod
    def clear_session():
        try:
            K.clear_session()
        except Exception as e:
            print(e)
