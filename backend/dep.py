"""
Electrical Component Classification - Prediction Module
Professional-grade prediction logic for electrical component classification.
"""

import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import json
import os
import logging
from typing import Tuple, Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ElectricalComponentPredictor:
    """
    Professional-grade electrical component classifier.
    
    This class handles model loading, image preprocessing, and prediction
    for electrical component classification using a pre-trained ResNet50 model.
    """
    
    def __init__(self, model_path: str, class_map_path: str, device: str = None):
        """
        Initialize the predictor with model and class mapping.
        
        Args:
            model_path (str): Path to the trained model weights
            class_map_path (str): Path to the class mapping JSON file
            device (str, optional): Device to run inference on ('cuda' or 'cpu')
        """
        self.model_path = model_path
        self.class_map_path = class_map_path
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.class_map = None
        self.transform = None
        
        # Initialize the predictor
        self._load_model()
        self._load_class_map()
        self._setup_transforms()
        
        logger.info(f"ElectricalComponentPredictor initialized on device: {self.device}")
    
    def _load_model(self) -> None:
        """Load the trained model with proper error handling."""
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file not found: {self.model_path}")
            
            # Load class mapping to get number of classes
            with open(self.class_map_path, 'r') as f:
                class_map = json.load(f)
            num_classes = len(class_map)
            
            # Create model architecture (matching training script)
            model = models.resnet50(weights=None)  # Don't load pretrained weights
            num_ftrs = model.fc.in_features
            
            # Custom classifier head (matching training architecture)
            model.fc = nn.Sequential(
                nn.Linear(num_ftrs, 512),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(512, num_classes)
            )
            
            # Load trained weights
            model.load_state_dict(torch.load(self.model_path, map_location=self.device))
            model.to(self.device)
            model.eval()
            
            self.model = model
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def _load_class_map(self) -> None:
        """Load the class mapping from JSON file."""
        try:
            if not os.path.exists(self.class_map_path):
                raise FileNotFoundError(f"Class map file not found: {self.class_map_path}")
            
            with open(self.class_map_path, 'r') as f:
                self.class_map = json.load(f)
            
            logger.info(f"Class map loaded with {len(self.class_map)} classes")
            
        except Exception as e:
            logger.error(f"Error loading class map: {str(e)}")
            raise
    
    def _setup_transforms(self) -> None:
        """Setup image preprocessing transforms."""
        self.transform = transforms.Compose([
            transforms.Resize((128, 256)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        logger.info("Image transforms configured")
    
    def preprocess_image(self, image_path: str) -> Optional[torch.Tensor]:
        """
        Preprocess an image for prediction.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            torch.Tensor: Preprocessed image tensor or None if error
        """
        try:
            # Validate file exists
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return None
            
            # Open and convert image
            image = Image.open(image_path).convert('RGB')
            
            # Apply transforms
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            logger.info(f"Image preprocessed successfully: {image_path}")
            return image_tensor
            
        except Exception as e:
            logger.error(f"Error preprocessing image {image_path}: {str(e)}")
            return None
    
    def predict(self, image_path: str) -> Dict[str, Any]:
        """
        Make a prediction on an image.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Dict[str, Any]: Prediction results with class name, confidence, and probabilities
        """
        try:
            # Preprocess image
            image_tensor = self.preprocess_image(image_path)
            if image_tensor is None:
                return {
                    'success': False,
                    'error': 'Failed to preprocess image',
                    'class_name': None,
                    'confidence': 0.0,
                    'probabilities': {}
                }
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted_idx = torch.max(probabilities, 1)
            
            # Get class name and create probability mapping
            predicted_class = self.class_map[str(predicted_idx.item())]
            confidence_score = confidence.item()
            
            # Create probability distribution for all classes
            prob_dist = {}
            for idx, class_name in self.class_map.items():
                prob_dist[class_name] = probabilities[0][int(idx)].item()
            
            # Sort probabilities for better display
            sorted_probs = sorted(prob_dist.items(), key=lambda x: x[1], reverse=True)
            
            result = {
                'success': True,
                'class_name': predicted_class,
                'confidence': confidence_score,
                'probabilities': dict(sorted_probs[:5]),  # Top 5 predictions
                'all_probabilities': prob_dist
            }
            
            logger.info(f"Prediction successful: {predicted_class} (confidence: {confidence_score:.4f})")
            return result
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'class_name': None,
                'confidence': 0.0,
                'probabilities': {}
            }
    
    def get_class_info(self) -> Dict[str, Any]:
        """
        Get information about available classes.
        
        Returns:
            Dict[str, Any]: Class information
        """
        return {
            'num_classes': len(self.class_map),
            'classes': list(self.class_map.values()),
            'class_mapping': self.class_map
        }


def create_predictor(model_path: str = None, class_map_path: str = None) -> ElectricalComponentPredictor:
    """
    Factory function to create a predictor instance.
    
    Args:
        model_path (str, optional): Path to model file
        class_map_path (str, optional): Path to class map file
        
    Returns:
        ElectricalComponentPredictor: Initialized predictor instance
    """
    # Default paths
    if model_path is None:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'electrical_component_classifier.pth')
    if class_map_path is None:
        class_map_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'class_map.json')
    
    return ElectricalComponentPredictor(model_path, class_map_path)


# Example usage and testing
if __name__ == "__main__":
    try:
        # Create predictor
        predictor = create_predictor()
        
        # Get class information
        class_info = predictor.get_class_info()
        print(f"Available classes: {class_info['num_classes']}")
        print(f"Classes: {class_info['classes']}")
        
        # Test prediction (you would replace this with an actual image path)
        test_image = "path/to/your/test/image.jpg"
        if os.path.exists(test_image):
            result = predictor.predict(test_image)
            print(f"Prediction result: {result}")
        else:
            print("No test image found. Please provide a valid image path.")
            
    except Exception as e:
        print(f"Error in main: {str(e)}")
