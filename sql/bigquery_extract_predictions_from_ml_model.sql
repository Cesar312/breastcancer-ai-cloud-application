-- BigQuery ML DNN Classifier Model: Extract Predictions

SELECT
  prediction.label AS predicted_label,
  prediction.prob AS probability,
  *
FROM ML.PREDICT(MODEL `uci_bcds.dnn_classifier_scaled`,
  (
    SELECT
    Record_Id,
      Clump_thickness AS scaled_Clump_thickness,
      Uniformity_of_cell_size AS scaled_Uniformity_of_cell_size,
      Uniformity_of_cell_shape AS scaled_Uniformity_of_cell_shape,
      Marginal_adhesion AS scaled_Marginal_adhesion,
      Single_epithelial_cell_size AS scaled_Single_epithelial_cell_size,
      Bare_nuclei AS scaled_Bare_nuclei,
      Bland_chromatin AS scaled_Bland_chromatin,
      Normal_nucleoli AS scaled_Normal_nucleoli,
      Mitoses AS scaled_Mitoses
    FROM 
      `bigquery-wk4.uci_bcds.raw_mm_ds`
  ) 
)
 , UNNEST(predicted_isMalignant_probs) AS PREDICTION;