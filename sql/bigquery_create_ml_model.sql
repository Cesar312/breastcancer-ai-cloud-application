-- Create BigQuery ML DNN Classifier Model on Scaled Data

CREATE OR REPLACE MODEL `uci_bcds.dnn_classifier_scaled`

OPTIONS (
  MODEL_TYPE = 'DNN_CLASSIFIER', 
  ACTIVATION_FN = 'RELU',               -- Activiation Function
  DROPOUT = 0.1,                        -- Droput Rate
  EARLY_STOP = TRUE,
  HIDDEN_UNITS = [128, 128],            -- Hidden Layers
  INPUT_LABEL_COLS = ['isMalignant'],   
  MAX_ITERATIONS = 50,                  
  OPTIMIZER = 'ADAM'                    
  )

AS
SELECT
  IF (Class = 2, 0, 1) AS isMalignant,
  ML.STANDARD_SCALER(Clump_thickness) OVER() AS scaled_Clump_thickness,
  ML.STANDARD_SCALER(Uniformity_of_cell_size) OVER() AS scaled_Uniformity_of_cell_size,
  ML.STANDARD_SCALER(Uniformity_of_cell_shape) OVER() AS scaled_Uniformity_of_cell_shape,
  ML.STANDARD_SCALER(Marginal_adhesion) OVER() AS scaled_Marginal_adhesion,
  ML.STANDARD_SCALER(Single_epithelial_cell_size) OVER() AS scaled_Single_epithelial_cell_size,
  ML.STANDARD_SCALER(Bare_nuclei) OVER() AS scaled_Bare_nuclei,
  ML.STANDARD_SCALER(Bland_chromatin) OVER() AS scaled_Bland_chromatin,
  ML.STANDARD_SCALER(Normal_nucleoli) OVER() AS scaled_Normal_nucleoli,
  ML.STANDARD_SCALER(Mitoses) OVER() AS scaled_Mitoses
FROM
  `bigquery-wk4.uci_bcds.mm_ds`;