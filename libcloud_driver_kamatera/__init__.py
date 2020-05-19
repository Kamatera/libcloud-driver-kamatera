from libcloud.compute import providers


KAMATERA_NODE_DRIVER = "kamatera_node_driver"


providers.set_driver(KAMATERA_NODE_DRIVER, "libcloud_driver_kamatera.kamatera", "KamateraNodeDriver")


def get_node_driver():
    return providers.get_driver(KAMATERA_NODE_DRIVER)
