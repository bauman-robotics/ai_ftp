#!/usr/bin/env python
# coding: utf-8

# In[26]:

def main():
    from tensorflow.keras.datasets import mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    import matplotlib.pyplot as plt
    #-----------------
    from tensorflow import keras
    from tensorflow.keras import layers
    #-----------------
    import numpy as np
    from PIL import Image 
    #-----------------
    import os
    
    #path = os.getcwd()
    path = os.path.dirname(os.path.abspath(__file__)) 

    # In[27]:
    
    
    #===== Old Model =====================
    # #--- create model --------------
    # model = keras.Sequential([
    # layers.Dense(512, activation="relu"),
    # layers.Dense(10, activation="softmax")
    # ])
    # #----- compile model -----------
    # model.compile(optimizer="rmsprop",
    # loss="sparse_categorical_crossentropy",
    # metrics=["accuracy"])
    #-------------------------------
    # #-----------------------------------------------
    # # Восстановление состояния модели
    # model_file = path + '/my_model.keras'
    # print("model_file_name=", model_file)
    # model = keras.models.load_model(model_file)
    # #-----------------------------------------------
    # #model.summary()
    
    #====================================
    
    
    # In[28]:
    
    
    #===== New Model =====================
    type(train_images)
    print('dtype =', train_images.dtype)
    print('ndim =', train_images.ndim)
    print('shape =', train_images.shape)
    
    #train_images = train_images.reshape((60000, 28 * 28))
    train_images = train_images.astype('float32') / 255
    #test_images = test_images.reshape((10000, 28 * 28))
    test_images = test_images.astype('float32') / 255
    
    # Создание свёрточной нейросети  ======= GPT =======
    model = keras.Sequential([
        # Свёрточный слой
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        
        # Слой пулинга
        layers.MaxPooling2D((2, 2)),
        # Свёрточный слой
        layers.Conv2D(64, (3, 3), activation='relu'),
        # Слой пулинга
        layers.MaxPooling2D((2, 2)),
        # Свёрточный слой
        layers.Conv2D(64, (3, 3), activation='relu'),
        # Преобразование данных из 2D в 1D
        layers.Flatten(),
        # Полносвязный слой
        layers.Dense(64, activation='relu'),
        # Выходной слой
        layers.Dense(10, activation='softmax')
    ])
    
    # Компиляция модели
    model.compile(optimizer='rmsprop',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    # Вывод информации о модели
    model.summary()
    
    
    # In[29]:
    
    
    #===== New Model =====================
    # # Восстановление состояния модели ================================= GPT 
    model_file = path + '/my_model.keras'
    if os.path.exists(model_file):
        model = keras.models.load_model(model_file)
    else:
        print("The model file does not exist, training a new model.")
        #===== New Model =====================
        model.fit(train_images, train_labels, epochs=5, batch_size=128) 
        
    # Вывод структуры модели
    model.summary()
    # Объяснение изменений:
    # Изменение формы входных данных: Так как свёрточные слои ожидают входные данные 
    # в формате (height, width, channels), 
    # мы изменили форму обучающих и тестовых изображений 
    # с (60000, 28, 28) на (60000, 28, 28, 1) и (10000, 28, 28, 1) соответственно.
    
    
    # In[30]:
    
    
    #################################################################################
    #################################################################################
    #################################################################################
    #=== Get Test Imgs Names and Valid Count ===
    import folder_funcs
    import numpy as np
    import os           # temp 
    print('path = ', path)
    f_name_ok  = ['' for _ in range(folder_funcs.MAX_COUNT_TEST_IMGS)]
    
    f_ok_count = folder_funcs.Test_Imgs_Get(path, f_name_ok)
    
    #print(str(folder_funcs.MAX_COUNT_TEST_IMGS))
    print("count right test_files = ", str(f_ok_count))
    # print("1_file_name = ", f_name_ok[0])
    
    
    # In[31]:
    
    
    #=== Get Test Imgs ===
    test_file_folder_path = folder_funcs.Get_Input_Folder_Path()
    
    test_imgs  = ['' for _ in range(f_ok_count)]
    imgs  = np.zeros((f_ok_count,28,28))
    for i in range(f_ok_count) :
        test_imgs[i] = np.asarray(Image.open(test_file_folder_path + f_name_ok[i]).convert('L'))
        imgs[i] = np.invert(test_imgs[i])
        imgs[i] = imgs[i].astype('float32') / 255
    
    
    # In[32]:
    
    
    #=== plot Test Imgs ===
    
    plt_w_count = 5
    plt_h_count = 2
    fig, axes = plt.subplots(plt_h_count, plt_w_count, figsize=(6, 3))
    ax = axes.ravel()
    
    if (f_ok_count > 10) :
        plot_count = 10
    else :
        plot_count = f_ok_count
        
    for i in range(plot_count) :    
        ax[i].imshow(imgs[i], cmap=plt.cm.gray)
        ax[i].set_title(str(f_name_ok[i]))
    
    fig.tight_layout()
    #plt.show()
    #=== save plot Test Imgs ===
    import folder_funcs
    output_folder = folder_funcs.Get_Output_Folder_Path() 
    print(output_folder)
    output_plt_name = output_folder + 'plt.png'
    print(output_plt_name)
    fig.savefig(path + output_plt_name)
    #fig.savefig('Upload/' + 'plt.png')
    
    
    # In[33]:
    
    
    #===== Old Model =====================
    # #=== Reshape ====
    # print('imgs.dim =', imgs[0].ndim) 
    # print('imgs.shape =', imgs[0].shape) 
    # imgs = imgs.reshape((f_ok_count, folder_funcs.file_h * folder_funcs.file_w)) 
    # print('test_imgs.dim =', imgs[0].ndim) 
    # print('test_imgs.shape =', imgs.shape) 
    
    
    # In[34]:
    
    
    if (f_ok_count > 0):
        predictions = model.predict(imgs)
    
    
    # In[35]:
    
    
    #=== Save results to file ===
    import folder_funcs
    if (f_ok_count > 0):
        folder_funcs.write_table(predictions)
    
    
    # In[36]:
    
    
    model.save(model_file)
    
    
    # In[25]:
    
    
    #------------------------------------------------------
    #=== For genarated script self_img_test.py uncomment line below
    
    #!jupyter nbconvert --to script self_img_test.ipynb
    
    # if was generated script self_img_test.py 
    # need add folow below to script self_img_test.ipynb
    
    # def main():
    #     all content of script script self_img_test.py 
    #     pass
    
    # if __name__ == '__main__':
    #     main()  # скрипт запускается непосредственно
    #------------------------------------------------------
    
    
    # In[ ]:

    pass

if __name__ == '__main__':
    main()  # скрипт запускается непосредственно


