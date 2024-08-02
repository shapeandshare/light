from shapeandshare.darkness import Island, Tile

from ..dtos.center_dim import CenterDim
from ..dtos.center_metadata import CenterMetadata
from .tile import TileSprite


class SpriteIsland(Island):
    tiles: dict[str, TileSprite] = {}

    # there can be only one
    hovered_tile_id: str | None = None
    selected_tile_id: str | None = None

    # canvas offset
    offset: tuple[int, int]

    @property
    def offset_x(self) -> int:
        x, _ = self.offset
        return x

    @property
    def offset_y(self) -> int:
        _, y = self.offset
        return y

    def load_tiles(self, tiles=dict[str, Tile]) -> None:
        max_x, max_y = self.dimensions
        for x in range(max_x):
            for y in range(max_y):
                tile_name: str = f"tile_{x}_{y}"
                tile = tiles[tile_name]
                tile_partial: dict = tile.model_dump()
                tile_partial["center"] = self._tile_center(itr_x=x, itr_y=y)
                tile_sprite: TileSprite = TileSprite.model_validate(tile_partial)
                self.tiles[tile_sprite.id] = tile_sprite

    def _tile_center(self, itr_x: int, itr_y: int) -> CenterMetadata:
        return CenterMetadata(
            x=CenterDim(offset=self.offset_x, itr=itr_x), y=CenterDim(offset=self.offset_y, itr=itr_y)
        )

    def _hover_over_tile(self, id: str) -> None:
        self.tiles[id].hover()

    def _unhover_over_tile(self, id: str) -> None:
        if id and id in self.tiles.keys():
            self.tiles[id].unhover()

    def _hovered_over(self, position: tuple[int, int]) -> str | None:
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

    def update_tile_selection(self, position: tuple[int, int]) -> None:
        tile_id: str | None = self._hovered_over(position=position)
        # print(f"selected tile: {self.selected_tile_id} -> {tile_id}")
        # Then we are selecting
        if self.selected_tile_id == tile_id:
            # then we are unselecting
            # print(f"explicitly unselecting {tile_id}")
            self._unhover_over_tile(id=self.selected_tile_id)
            self.selected_tile_id = None
        elif self.selected_tile_id != tile_id:
            # then we need to match a change
            if self.selected_tile_id:
                # print(f"implicitly unselecting {tile_id}")
                self._unhover_over_tile(id=self.selected_tile_id)
            if tile_id:
                self.selected_tile_id = tile_id
                # print(f"selecting {tile_id}")
                self._hover_over_tile(id=self.selected_tile_id)

    def update_tile_hover(self, position: tuple[int, int]):
        pass
        tile_id: str | None = self._hovered_over(position=position)

        # Then we are hovering
        if self.hovered_tile_id != tile_id:
            # then we need to match a change
            if self.hovered_tile_id and self.hovered_tile_id != self.selected_tile_id:
                self._unhover_over_tile(id=self.hovered_tile_id)
            if tile_id:
                self.hovered_tile_id = tile_id
                self._hover_over_tile(id=self.hovered_tile_id)
