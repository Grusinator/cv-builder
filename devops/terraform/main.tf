provider "azurerm" {
  features {}
}

provider "azuread" {
  tenant_id = data.azurerm_client_config.current.tenant_id
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "cv_builder" {
  name     = "cv-builder-resources"
  location = "West Europe"
}

resource "azurerm_service_plan" "cv_builder" {
  name                = "cv-builder-appserviceplan"
  location            = azurerm_resource_group.cv_builder.location
  resource_group_name = azurerm_resource_group.cv_builder.name
  os_type             = "Linux"
  sku_name            = "F1"  # Free tier
}

resource "azurerm_linux_web_app" "cv_builder" {
  name                = "cv-builder-appservice"
  location            = azurerm_resource_group.cv_builder.location
  resource_group_name = azurerm_resource_group.cv_builder.name
  service_plan_id     = azurerm_service_plan.cv_builder.id

  site_config {
    always_on = true
    # This line is removed because it's set automatically
    # linux_fx_version = "PYTHON|3.11"
  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "PYTHON_VERSION" = "3.11"
  }
}

resource "azuread_application" "cv_builder" {
  display_name = "cv-builder-app"
}

resource "azuread_service_principal" "cv_builder" {
  application_object_id = azuread_application.cv_builder.id
}

resource "azuread_service_principal_password" "cv_builder" {
  service_principal_id = azuread_service_principal.cv_builder.id
  end_date             = "2099-01-01T00:00:00Z"
}

resource "random_password" "cv_builder" {
  length  = 16
  special = true
}

output "client_id" {
  value = azuread_service_principal.cv_builder.id
}

output "client_secret" {
  value     = azuread_service_principal_password.cv_builder.value
  sensitive = true
}

output "tenant_id" {
  value = data.azurerm_client_config.current.tenant_id
}
