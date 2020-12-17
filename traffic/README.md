The convolutional neural network model is based on the TensorFlow Keras Sequential Model.
1. I started by applying: **one** convolutional layer with 32 filters and a 3x3 kernel,
**one** max-pooling layer with 2x2 pool size, **one** hidden layer with 128 units and a 0.5 dropout.
   The results showed that the setting was certainly insufficient to learn for the data set. 
   This reason for this was probably that one convolutional layer and one pooling layer did not generalize the image enough,
   meaning that the images were too specific for the model to predict for other images. 
   Also, only one hidden was certainly insufficient for such a complex data set.
   
        Epoch 1/10
        497/497 [==============================] - 4s 8ms/step - loss: 5.1429 - accuracy: 0.0524
        Epoch 2/10
        497/497 [==============================] - 4s 8ms/step - loss: 3.5696 - accuracy: 0.0562
        Epoch 3/10
        497/497 [==============================] - 4s 8ms/step - loss: 3.5213 - accuracy: 0.0557
        Epoch 4/10
        497/497 [==============================] - 4s 8ms/step - loss: 3.4990 - accuracy: 0.0562
        Epoch 5/10
        497/497 [==============================] - 4s 8ms/step - loss: 3.4888 - accuracy: 0.0562
        Epoch 6/10
        497/497 [==============================] - 4s 8ms/step - loss: 3.4841 - accuracy: 0.0562
        Epoch 7/10
        497/497 [==============================] - 4s 7ms/step - loss: 3.4817 - accuracy: 0.0554
        Epoch 8/10
        497/497 [==============================] - 4s 7ms/step - loss: 3.4806 - accuracy: 0.0555
        Epoch 9/10
        497/497 [==============================] - 4s 8ms/step - loss: 3.4800 - accuracy: 0.0562
        Epoch 10/10
        497/497 [==============================] - 4s 8ms/step - loss: 3.4797 - accuracy: 0.0556
        331/331 - 1s - loss: 3.4837 - accuracy: 0.0574
2. I then experimented by adding **two more** hidden layers with 128 units and the same relu activation. 
   The results were much better, but there was still lots of room for improvement. 
   Having more layers made the model train itself better on the variety of signs in the data set. 
   However, it seems to make it harder to train the model and there is also a risk over-fitting.
   
        Epoch 1/10
        497/497 [==============================] - 3s 7ms/step - loss: 3.7887 - accuracy: 0.3184
        Epoch 2/10
        497/497 [==============================] - 4s 7ms/step - loss: 1.1334 - accuracy: 0.6863
        Epoch 3/10
        497/497 [==============================] - 4s 7ms/step - loss: 0.7232 - accuracy: 0.7994
        Epoch 4/10
        497/497 [==============================] - 4s 8ms/step - loss: 0.5114 - accuracy: 0.8585
        Epoch 5/10
        497/497 [==============================] - 4s 7ms/step - loss: 0.4451 - accuracy: 0.8780
        Epoch 6/10
        497/497 [==============================] - 3s 7ms/step - loss: 0.3738 - accuracy: 0.9002
        Epoch 7/10
        497/497 [==============================] - 3s 7ms/step - loss: 0.3427 - accuracy: 0.9118
        Epoch 8/10
        497/497 [==============================] - 3s 7ms/step - loss: 0.3127 - accuracy: 0.9209
        Epoch 9/10
        497/497 [==============================] - 3s 7ms/step - loss: 0.2487 - accuracy: 0.9326
        Epoch 10/10
        497/497 [==============================] - 3s 7ms/step - loss: 0.2330 - accuracy: 0.9395
        331/331 - 1s - loss: 0.3226 - accuracy: 0.9295
3. With the idea of avoiding over-fitting in mind, I decided to add more dropout layers. 
   I ended up adding **two more dropout** layers after two last hidden layers. The probability I set was 0.05, for both.
   It actually seemed to worsen the situation. 
   I think the problem was that having so many dropouts did not let the model train properly.
   
        Epoch 1/10
        497/497 [==============================] - 3s 7ms/step - loss: 3.7303 - accuracy: 0.3614 
        Epoch 2/10
        497/497 [==============================] - 3s 7ms/step - loss: 0.9538 - accuracy: 0.7256
        Epoch 3/10
        497/497 [==============================] - 3s 7ms/step - loss: 0.6060 - accuracy: 0.8304
        Epoch 4/10
        497/497 [==============================] - 3s 7ms/step - loss: 0.4416 - accuracy: 0.8770
        Epoch 5/10
        497/497 [==============================] - 3s 7ms/step - loss: 0.3713 - accuracy: 0.9000
        Epoch 6/10
        497/497 [==============================] - 3s 7ms/step - loss: 0.3290 - accuracy: 0.9122
        Epoch 7/10
        497/497 [==============================] - 3s 7ms/step - loss: 0.2751 - accuracy: 0.9240
        Epoch 8/10
        497/497 [==============================] - 3s 7ms/step - loss: 0.2726 - accuracy: 0.9277
        Epoch 9/10
        497/497 [==============================] - 3s 7ms/step - loss: 0.2379 - accuracy: 0.9377
        Epoch 10/10
        497/497 [==============================] - 3s 7ms/step - loss: 0.2009 - accuracy: 0.9458
        331/331 - 1s - loss: 0.4967 - accuracy: 0.8976
4. Finally, I decided to have only **one** dropout of 0.5 probability and add another convolutional layer to generalize the images better.
   Having **two** convolutional layers, one before the pooling layer and another after, helped to have a better accuracy.
   The extra convolutional layer probably helped by making the images look more like other images, which is useful for the model.
   
        Epoch 1/10
        497/497 [==============================] - 4s 8ms/step - loss: 2.4592 - accuracy: 0.4404
        Epoch 2/10
        497/497 [==============================] - 4s 8ms/step - loss: 0.7963 - accuracy: 0.7889
        Epoch 3/10
        497/497 [==============================] - 4s 8ms/step - loss: 0.4611 - accuracy: 0.8777
        Epoch 4/10
        497/497 [==============================] - 5s 9ms/step - loss: 0.3431 - accuracy: 0.9078
        Epoch 5/10
        497/497 [==============================] - 4s 9ms/step - loss: 0.2949 - accuracy: 0.9218
        Epoch 6/10
        497/497 [==============================] - 4s 9ms/step - loss: 0.2282 - accuracy: 0.9379
        Epoch 7/10
        497/497 [==============================] - 5s 9ms/step - loss: 0.2098 - accuracy: 0.9454
        Epoch 8/10
        497/497 [==============================] - 5s 9ms/step - loss: 0.1898 - accuracy: 0.9526
        Epoch 9/10
        497/497 [==============================] - 4s 9ms/step - loss: 0.1748 - accuracy: 0.9544
        Epoch 10/10
        497/497 [==============================] - 5s 10ms/step - loss: 0.1630 - accuracy: 0.9581
        331/331 - 1s - loss: 0.2204 - accuracy: 0.9536
5. Actually, it seems like having **another pooling layer** after the second convolutional layer helps to lower the loss while preserving the accuracy. 
        
        Epoch 1/10
        497/497 [==============================] - 3s 7ms/step - loss: 2.8686 - accuracy: 0.3052 
        Epoch 2/10
        497/497 [==============================] - 4s 7ms/step - loss: 1.1733 - accuracy: 0.6533
        Epoch 3/10
        497/497 [==============================] - 4s 8ms/step - loss: 0.6370 - accuracy: 0.8115
        Epoch 4/10
        497/497 [==============================] - 4s 8ms/step - loss: 0.4136 - accuracy: 0.8793
        Epoch 5/10
        497/497 [==============================] - 4s 8ms/step - loss: 0.2983 - accuracy: 0.9171
        Epoch 6/10
        497/497 [==============================] - 4s 8ms/step - loss: 0.2715 - accuracy: 0.9251
        Epoch 7/10
        497/497 [==============================] - 4s 8ms/step - loss: 0.2239 - accuracy: 0.9393
        Epoch 8/10
        497/497 [==============================] - 4s 8ms/step - loss: 0.1857 - accuracy: 0.9497
        Epoch 9/10
        497/497 [==============================] - 4s 8ms/step - loss: 0.1619 - accuracy: 0.9581
        Epoch 10/10
        497/497 [==============================] - 4s 8ms/step - loss: 0.1507 - accuracy: 0.9604
        331/331 - 1s - loss: 0.1485 - accuracy: 0.9654
