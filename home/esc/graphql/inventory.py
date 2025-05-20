from .base import *

class Inventory(GraphQL):
    def inventory_level(self,id):
        return self.run(
        """
        query getInventoryLevel($id:ID!) {
            inventoryLevel(id: $id) {
                id
                quantities(names: ["available", "incoming", "committed", "damaged", "on_hand", "quality_control", "reserved", "safety_stock"]) {
                    name
                    quantity
                }
                item {
                    id
                    sku
                    inventoryHistoryUrl
                    variant {
                        id
                        product {
                            id
                            title
                            sellingPlanGroupCount {
                                count
                            }
                        }
                    }
                }
                location {
                    id
                    name
                }
            }
        }
        """,
            {
                "id":id,
            }
        )