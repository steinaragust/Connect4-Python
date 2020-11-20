import tensorflow.keras as keras

model = keras.models.load_model("model_24hour_1_final.h5",compile=False)

keras.utils.plot_model(model, "semi_az_nn.png")