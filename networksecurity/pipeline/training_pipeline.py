import os, sys

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import(
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainerConfig
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifacts,
)


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info(f"Start data ingestion")
            
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = DataValidationConfig(self.training_pipeline_config)
            logging.info("Data validation initiated")
            
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact, 
                data_validation_config=self.data_validation_config
                )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data validation completed")
            
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            self.data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            logging.info("Data transformation initiated")
            
            data_transformation = DataTransformation(
                data_validation_artifact=data_validation_artifact,
                data_transformation_config=self.data_transformation_config
                )
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data transformation completed")
            
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def model_training(self, data_transformation_artifact: DataTransformationArtifacts):
        try:
            model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            logging.info("Model training started")
            
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
            
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("Model Training Completed")
            
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.model_training(data_transformation_artifact=data_transformation_artifact)
            
            return model_trainer_artifact
        except Exception as e:
            NetworkSecurityException(e, sys)