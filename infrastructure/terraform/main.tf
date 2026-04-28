provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location
}

# Azure Kubernetes Service for Metadata Processing and Analytics
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "governance"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_DS3_v2"
  }

  identity {
    type = "SystemAssigned"
  }
}

# OpenSearch Cluster for Metadata Discovery and Search Relevance Benchmarking
resource "aws_opensearch_domain" "search" {
  domain_name    = "search-${var.project_name}-${var.environment}"
  engine_version = "OpenSearch_2.5"

  cluster_config {
    instance_type = "t3.medium.search"
    instance_count = 2
  }

  ebs_options {
    ebs_enabled = true
    volume_size = 20
  }
}

# Azure Storage for Immutable Metadata Backups and Governance Audit Logs
resource "azurerm_storage_account" "governance_data" {
  name                     = "st${var.project_name}${var.environment}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
