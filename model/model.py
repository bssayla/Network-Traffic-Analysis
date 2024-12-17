from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam

class ClassificationModel:
    def __init__(self, numerical_feature_count, num_classes):
        """
        Initializes the ClassificationModel class.
        
        :param numerical_feature_count: Number of numerical features.
        :param num_classes: Number of classes in the target variable.
        """
        self.numerical_feature_count = numerical_feature_count
        self.num_classes = num_classes
        self.model = self._build_model()

    def _build_model(self):
        """
        Builds the TensorFlow model for classification tasks.
        
        :return: Compiled TensorFlow model.
        """
        # Numerical input
        numerical_input = Input(shape=(self.numerical_feature_count,), name="numerical_input")
        x = BatchNormalization()(numerical_input)  # Normalize numerical inputs

        # Fully connected layers
        x = Dense(128, activation='relu')(x)
        x = Dropout(0.3)(x)
        x = Dense(64, activation='relu')(x)
        x = Dropout(0.3)(x)
        x = Dense(32, activation='relu')(x)

        # Output layer
        output = Dense(self.num_classes, activation='softmax', name="output")(x)

        # Create model
        model = Model(inputs=numerical_input, outputs=output)
        
        # Compile model
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model

    def summary(self):
        """Prints the summary of the model."""
        self.model.summary()

