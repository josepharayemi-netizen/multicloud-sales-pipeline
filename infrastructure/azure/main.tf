terraform {
  required_version = ">= 1.6"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 4.0" }
    random = { source = "hashicorp/random", version = "~> 3.0" }
  }
}
provider "azurerm" { features {} }
resource "random_string" "suffix" { length = 6; special = false; upper = false }
resource "azurerm_resource_group" "main" {
  name = "rg-${var.project_name}-${random_string.suffix.result}"
  location = var.location
}
resource "azurerm_storage_account" "main" {
  name = "${var.project_name}${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location = azurerm_resource_group.main.location
  account_tier = "Standard"
  account_replication_type = "LRS"
  min_tls_version = "TLS1_2"
  allow_nested_items_to_be_public = false
}
resource "azurerm_storage_container" "landing" {
  name = "landing"
  storage_account_id = azurerm_storage_account.main.id
  container_access_type = "private"
}
output "storage_account" { value = azurerm_storage_account.main.name }
