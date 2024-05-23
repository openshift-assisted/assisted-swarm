package inventory

import (
	"fmt"

	"github.com/openshift/assisted-installer-agent/src/config"
	"github.com/openshift/assisted-service/models"
)

func applyDryRunConfig(subprocessConfig *config.SubprocessConfig, inventory *models.Inventory) {
	targetInterface, err := findRelevantInterface(inventory)
	if err != nil {
		return
	}

	// Override the mac address & IPv4 address to the user requested one
	inventory.Interfaces[targetInterface].MacAddress = subprocessConfig.ForcedMacAddress
	inventory.Interfaces[targetInterface].IPV4Addresses[0] = subprocessConfig.ForcedHostIPv4
	inventory.Interfaces[targetInterface].IPV6Addresses[0] = subprocessConfig.ForcedHostIPv6

	// Throw away other interfaces to avoid some exotic bugs relating to duplicate mac addreses from two different hosts
	inventory.Interfaces = []*models.Interface{inventory.Interfaces[targetInterface]}
}

// findRelevantInterface returns the index of the first interface
// which has an ipv4 address
func findRelevantInterface(inventory *models.Inventory) (int, error) {
	for interfaceIndex, iface := range inventory.Interfaces {
		if iface.Type == "physical" && len(iface.IPV4Addresses) > 0 {
			return interfaceIndex, nil
		}
	}

	return -1, fmt.Errorf("no suitable interface for dry run reconfiguration found in %+v", inventory.Interfaces)
}
