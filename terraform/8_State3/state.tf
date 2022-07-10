

terraform {
    backend "s3" {
        bucket = "ej838639-terraform-state"
        key = "myproject.state"
        region = "eu-west-1"
    }
}