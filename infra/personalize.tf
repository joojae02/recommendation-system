resource "awscc_personalize_dataset_group" "recommendation_group" {
  name = "${var.project_name}-dataset-group-${var.environment}"
  depends_on = [
    aws_s3_object.users_data,
    aws_s3_object.items_data,
    aws_s3_object.interactions_data
  ]
}

resource "awscc_personalize_schema" "user_schema" {
  name = "${var.project_name}-user-schema-${var.environment}"
  schema = file("${path.module}/schemas/user-schema.json")
}

resource "awscc_personalize_schema" "item_schema" {
  name = "${var.project_name}-item-schema-${var.environment}"
  schema = file("${path.module}/schemas/item-schema.json")
}

resource "awscc_personalize_schema" "interactions_schema" {
  name = "${var.project_name}-interactions-schema-${var.environment}"
  schema = file("${path.module}/schemas/interaction-schema.json")
}

resource "awscc_personalize_dataset" "users" {
  name               = "${var.project_name}-users-dataset-${var.environment}"
  dataset_group_arn  = awscc_personalize_dataset_group.recommendation_group.dataset_group_arn
  dataset_type       = "Users"
  schema_arn         = awscc_personalize_schema.user_schema.schema_arn
  depends_on         = [
    awscc_personalize_dataset_group.recommendation_group,
    awscc_personalize_schema.user_schema
  ]
}

resource "awscc_personalize_dataset" "items" {
  name               = "${var.project_name}-items-dataset-${var.environment}"
  dataset_group_arn  = awscc_personalize_dataset_group.recommendation_group.dataset_group_arn
  dataset_type       = "Items"
  schema_arn         = awscc_personalize_schema.item_schema.schema_arn
  depends_on         = [
    awscc_personalize_dataset_group.recommendation_group,
    awscc_personalize_schema.item_schema
  ]
}

resource "awscc_personalize_dataset" "interactions" {
  name               = "${var.project_name}-interactions-dataset-${var.environment}"
  dataset_group_arn  = awscc_personalize_dataset_group.recommendation_group.dataset_group_arn
  dataset_type       = "Interactions" 
  schema_arn         = awscc_personalize_schema.interactions_schema.schema_arn
  depends_on         = [
    awscc_personalize_dataset_group.recommendation_group,
    awscc_personalize_schema.interactions_schema
  ]
}

# resource "awscc_personalize_solution" "recommendation_solution" {
#   name = "${var.project_name}-recommendation-solution-${var.environment}"
#   dataset_group_arn = awscc_personalize_dataset_group.recommendation_group.dataset_group_arn
#   recipe_arn = "arn:aws:personalize:::recipe/aws-user-personalization"  # 기본 사용자 개인화 레시피 사용

#   solution_config = {
#     algorithm_hyper_parameters = {
#       "hidden_dimension" = "32"
#       "bptt" = "32"
#       "recency_mask" = "true"
#     }
#   }
#   depends_on = [
#     awscc_personalize_dataset.users,
#     awscc_personalize_dataset.items,
#     awscc_personalize_dataset.interactions
#   ]
# } 