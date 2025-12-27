import joblib
import numpy as np
import os

class ServiceRecommendationSystem:
    """ML-based service recommendation system for vehicles"""
    
    def __init__(self):
        self.model = None
        self.mlb = None
        self.company_encoder = None
        self.model_encoder = None
        self.feature_info = None
        self.is_loaded = False
        
    def load_model(self):
        """Load the trained model and encoders"""
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))

            model_path = os.path.join(BASE_DIR, 'service_recommendation_model.pkl')
            mlb_path = os.path.join(BASE_DIR, 'mlb_encoder.pkl')
            company_path = os.path.join(BASE_DIR, 'company_encoder.pkl')
            model_enc_path = os.path.join(BASE_DIR, 'model_encoder.pkl')
            feature_path = os.path.join(BASE_DIR, 'feature_info.pkl')
            
            # Check if all files exist
            required_files = [model_path, mlb_path, company_path, model_enc_path, feature_path]
            for file in required_files:
                if not os.path.exists(file):
                    print(f"Warning: {file} not found. Please train the model first.")
                    return False
            
            # Load all components
            self.model = joblib.load(model_path)
            self.mlb = joblib.load(mlb_path)
            self.company_encoder = joblib.load(company_path)
            self.model_encoder = joblib.load(model_enc_path)
            self.feature_info = joblib.load(feature_path)
            
            self.is_loaded = True
            print("✅ ML model loaded successfully")
            return True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def extract_company_from_model(self, model_name):
        """Extract company name from model string"""
        model_lower = model_name.lower()
        
        # Honda models
        honda_models = ['amaze', 'city', 'civic', 'jazz', 'wr-v', 'cr-v', 'accord']
        if any(m in model_lower for m in honda_models):
            return 'Honda'
        
        # Tata models
        tata_models = ['tiago', 'nexon', 'harrier', 'safari', 'altroz']
        if any(m in model_lower for m in tata_models):
            return 'Tata'
        
        # Maruti models
        maruti_models = ['swift', 'baleno', 'alto', 'wagonr', 'dzire', 'vitara brezza', 'brezza']
        if any(m in model_lower for m in maruti_models):
            return 'Maruti'
        
        # Hyundai models
        hyundai_models = ['i10', 'i20', 'creta', 'venue', 'verna', 'tucson']
        if any(m in model_lower for m in hyundai_models):
            return 'Hyundai'
        
        # Toyota models
        toyota_models = ['innova', 'fortuner', 'glanza', 'urban cruiser', 'camry']
        if any(m in model_lower for m in toyota_models):
            return 'Toyota'
        
        # Default to Honda if not found
        return 'Honda'
    
    def predict_service_issues(self, model_name, year, mileage):
        """
        Predict service issues for a vehicle
        
        Parameters:
        - model_name: Vehicle model (e.g., "Honda Amaze")
        - year: Manufacturing year
        - mileage: Current mileage in km
        
        Returns:
        - List of predicted service issues
        """
        if not self.is_loaded:
            if not self.load_model():
                return []
        
        try:
            # Extract company from model name
            company = self.extract_company_from_model(model_name)
            
            # Calculate vehicle age
            current_year = 2024
            vehicle_age = current_year - int(year)
            
            # Encode company
            if company in self.company_encoder.classes_:
                company_encoded = self.company_encoder.transform([company])[0]
            else:
                # Use most common company as fallback
                company_encoded = self.company_encoder.transform(['Honda'])[0]
            
            # Encode model - simplified approach
            # Try to find exact match first
            model_simple = model_name.split()[-1] if ' ' in model_name else model_name
            
            if model_simple in self.model_encoder.classes_:
                model_encoded = self.model_encoder.transform([model_simple])[0]
            else:
                # Use a default model for the company
                default_models = {
                    'Honda': 'Amaze',
                    'Tata': 'Tiago',
                    'Maruti': 'Swift',
                    'Hyundai': 'i20',
                    'Toyota': 'Innova'
                }
                default_model = default_models.get(company, 'Amaze')
                if default_model in self.model_encoder.classes_:
                    model_encoded = self.model_encoder.transform([default_model])[0]
                else:
                    model_encoded = 0  # Fallback to first model
            
            # Create feature vector
            features = np.array([[
                company_encoded,
                model_encoded,
                int(year),
                vehicle_age,
                int(mileage)
            ]])
            
            # Predict
            prediction = self.model.predict(features)
            
            # Convert binary predictions to issue names
            predicted_issues = self.mlb.inverse_transform(prediction)[0]
            
            # Return as list
            return list(predicted_issues) if predicted_issues else []
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            return []
    
    def get_issue_priorities(self, issues, vehicle_age, mileage):
        """
        Categorize issues by priority
        
        Returns dict with 'high', 'medium', 'low' priority issues
        """
        high_priority = []
        medium_priority = []
        low_priority = []
        
        high_priority_keywords = [
            'brake', 'timing belt', 'clutch', 'battery', 'suspension',
            'transmission', 'exhaust', 'shock absorber'
        ]
        
        low_priority_keywords = [
            'wiper', 'headlight', 'bulb', 'tire rotation', 'air filter'
        ]
        
        for issue in issues:
            issue_lower = issue.lower()
            
            # Check for high priority
            if any(keyword in issue_lower for keyword in high_priority_keywords):
                high_priority.append(issue)
            # Check for low priority
            elif any(keyword in issue_lower for keyword in low_priority_keywords):
                low_priority.append(issue)
            # Everything else is medium
            else:
                medium_priority.append(issue)
        
        return {
            'high': high_priority,
            'medium': medium_priority,
            'low': low_priority
        }

# Create global instance
ml_system = ServiceRecommendationSystem()
