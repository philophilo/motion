data "archive_file" "motion_app" {
  type        = "zip"
  source_file = "../app/motion.py"
  output_path = "../app/motion.zip"
}