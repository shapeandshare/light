from shapeandshare.darkness import Island, Tile

from ..dtos.center_dim import CenterDim
from ..dtos.center_metadata import CenterMetadata
from .tile import TileSprite


class SpriteIsland(Island):
    tiles: dict[str, TileSprite] = {}

    # canvas offset
    offset: tuple[int, int]

    @property
    def offset_x(self) -> int:
        return self.offset[0]

    @property
    def offset_y(self) -> int:
        return self.offset[1]

    def load_tiles(self, tiles=dict[str, Tile]) -> None:
        max_x, max_y = self.dimensions
        for x in range(max_x):
            for y in range(max_y):
                tile_name: str = f"tile_{x}_{y}"
                tile = tiles[tile_name]
                tile_partial: dict = tile.model_dump()
                tile_partial["center"] = self.tile_center(itr_x=x, itr_y=y)
                tile_sprite: TileSprite = TileSprite.model_validate(tile_partial)
                self.tiles[tile_sprite.id] = tile_sprite

    def tile_center(self, itr_x: int, itr_y: int) -> CenterMetadata:
        return CenterMetadata(
            x=CenterDim(offset=self.offset_x, itr=itr_x), y=CenterDim(offset=self.offset_y, itr=itr_y)
        )

    def hover_over_tile(self, id: str) -> None:
        self.tiles[id].hover()

    def unhover_over_tile(self, id: str) -> None:
        if id and id in self.tiles.keys():
            self.tiles[id].unhover()

    def hovered_over(self, position: tuple[int, int]) -> str | None:
        if len(self.tiles) < 1:
            return

        # assume all tiles have the same dimensions
        for any_tile in self.tiles.values():
            tile_width = any_tile.rect.width
            tile_height = any_tile.rect.height
            break

        mouse_x, mouse_y = position
        island_x, island_y = self.dimensions
        island_max_x = (island_x * tile_width) + self.offset_x
        island_max_y = (island_y * tile_height) + self.offset_y

        # See if the mouse cursor is above the island:
        if (
            (mouse_x >= self.offset_x)
            and (mouse_y >= self.offset_y)
            and (mouse_x <= island_max_x)
            and (mouse_y <= island_max_y)
        ):
            # see if the cursor is above a tile:
            for tile_id, tile in self.tiles.items():
                # print(f"reviewing tile id: {tile_id}")
                # print(tile)
                tile_center_x, tile_center_y = tile.rect.center
                tile_min_x = tile_center_x - (tile_width / 2)
                tile_max_x = tile_center_x + (tile_width / 2)
                tile_min_y = tile_center_y - (tile_height / 2)
                tile_max_y = tile_center_y + (tile_height / 2)
                if (tile_min_x <= mouse_x <= tile_max_x) and (tile_min_y <= mouse_y <= tile_max_y):
                    return tile_id
