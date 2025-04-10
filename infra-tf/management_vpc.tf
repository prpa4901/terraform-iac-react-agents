
provider "google" {
  project = var.project_id
  region  = "us-east1"
}

resource "google_compute_network" "management_vpc" {
  name                    = "management-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "management_subnet" {
  name          = "management-subnet"
  ip_cidr_range = "10.112.0.0/17"
  region        = "us-east1"
  network       = google_compute_network.management_vpc.id
}

resource "google_compute_router" "management_router" {
  name    = "management-router"
  network = google_compute_network.management_vpc.id
  region  = "us-east1"
}

