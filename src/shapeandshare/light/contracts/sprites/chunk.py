import logging
import sys

from shapeandshare.darkness import Chunk, StateClient, Tile, TileConnectionType

from ..dtos.center_dim import CenterDim
from ..dtos.center_metadata import CenterMetadata
from .tile import TileSprite

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# TODO: move to numpy ...
# print(sys.getrecursionlimit())
sys.setrecursionlimit(24000)


class SpriteChunk(Chunk):
    tiles: dict[str, TileSprite] = {}

    # indexes
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

    def load_tiles(self, tiles: dict[str, Tile]) -> None:
        # Define the maximum size
        width, height = self.dimensions
        tile_matrix: list[list[str | None]] = [[None for y in range(height)] for x in range(width)]

        def build_it(origin_x: int, origin_y: int, origin_tile: Tile):
            # print(f"build_it | origin_x: {origin_x}, origin_y: {origin_y}, origin_tile: {origin_tile}")
            tile_matrix[origin_x - 1][origin_y - 1] = origin_tile.id
            for conn, neighbor in origin_tile.next.items():
                if conn == TileConnectionType.UP:
                    new_x = origin_x
                    new_y = origin_y - 1
                    # print(f"[UP] new_x: {new_x}, new_y: {new_y}")
                    try:
                        if tile_matrix[new_x - 1][new_y - 1] is None:
                            tile_matrix[new_x - 1][new_y - 1] = tiles[neighbor].id
                            build_it(origin_x=new_x, origin_y=new_y, origin_tile=tiles[neighbor])
                    except IndexError as error:
                        msg: str = str(error)
                        logger.warning(msg)
                elif conn == TileConnectionType.DOWN:
                    new_x = origin_x
                    new_y = origin_y + 1
                    # print(f"[DOWN] new_x: {new_x}, new_y: {new_y}")
                    try:
                        if tile_matrix[new_x - 1][new_y - 1] is None:
                            tile_matrix[new_x - 1][new_y - 1] = tiles[neighbor].id
                            build_it(origin_x=new_x, origin_y=new_y, origin_tile=tiles[neighbor])
                    except IndexError as error:
                        msg: str = str(error)
                        logger.warning(msg)
                elif conn == TileConnectionType.LEFT:
                    new_x = origin_x - 1
                    new_y = origin_y
                    # print(f"[LEFT] new_x: {new_x}, new_y: {new_y}")
                    try:
                        if tile_matrix[new_x - 1][new_y - 1] is None:
                            tile_matrix[new_x - 1][new_y - 1] = tiles[neighbor].id
                            build_it(origin_x=new_x, origin_y=new_y, origin_tile=tiles[neighbor])
                    except IndexError as error:
                        msg: str = str(error)
                        logger.warning(msg)
                elif conn == TileConnectionType.RIGHT:
                    new_x = origin_x + 1
                    new_y = origin_y
                    # print(f"[RIGHT] new_x: {new_x}, new_y: {new_y}")
                    try:
                        if tile_matrix[new_x - 1][new_y - 1] is None:
                            tile_matrix[new_x - 1][new_y - 1] = tiles[neighbor].id
                            build_it(origin_x=new_x, origin_y=new_y, origin_tile=tiles[neighbor])
                    except IndexError as error:
                        msg: str = str(error)
                        logger.warning(msg)

        build_it(origin_x=1, origin_y=1, origin_tile=tiles[self.origin])

        for x in range(0, width):
            for y in range(0, height):
                local_x = x + 1
                local_y = y + 1
                try:
                    tile_id = tile_matrix[local_x - 1][local_y - 1]
                    tile: Tile = tiles[tile_id]

                    # get tile by offset

                    tile_partial: dict = tile.model_dump()
                    tile_partial["center"] = self._tile_center(itr_x=x, itr_y=y)
                    tile_sprite: TileSprite = TileSprite.model_validate(tile_partial)
                    self.tiles[tile_sprite.id] = tile_sprite

                except IndexError as error:
                    msg: str = str(error)
                    logger.warning(msg)

    def _tile_center(self, itr_x: int, itr_y: int) -> CenterMetadata:
        return CenterMetadata(x=CenterDim(offset=self.offset_x, itr=itr_x), y=CenterDim(offset=self.offset_y, itr=itr_y))

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
        chunk_x, chunk_y = self.dimensions
        chunk_max_x = (chunk_x * tile_width) + self.offset_x
        chunk_max_y = (chunk_y * tile_height) + self.offset_y

        # See if the mouse cursor is above the chunk:
        if (mouse_x >= self.offset_x) and (mouse_y >= self.offset_y) and (mouse_x <= chunk_max_x) and (mouse_y <= chunk_max_y):
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

    def update_tile_selection(self, position: tuple[int, int]) -> TileSprite | None:
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
                self.selected_tile_id = None
            if tile_id:
                self.selected_tile_id = tile_id
                # print(f"selecting {tile_id}")
                self._hover_over_tile(id=self.selected_tile_id)
        return self.get_selected_tile()

    def get_selected_tile(self) -> TileSprite | None:
        if self.selected_tile_id:
            return self.tiles[self.selected_tile_id]

    def update_tile_hover(self, position: tuple[int, int]):
        tile_id: str | None = self._hovered_over(position=position)

        # Then we are hovering
        if self.hovered_tile_id != tile_id:
            # then we need to match a change
            if self.hovered_tile_id and self.hovered_tile_id != self.selected_tile_id:
                self._unhover_over_tile(id=self.hovered_tile_id)
            if tile_id:
                self.hovered_tile_id = tile_id
                self._hover_over_tile(id=self.hovered_tile_id)

    async def reload_tiles(self, client: StateClient, world_id: str, chunk_id: str) -> None:
        chunk: Chunk = await client.chunk_get(world_id=world_id, chunk_id=chunk_id, full=True)
        self.load_tiles(tiles=chunk.contents)
        if self.selected_tile_id:
            self._hover_over_tile(id=self.selected_tile_id)
        if self.hovered_tile_id:
            self._hover_over_tile(id=self.hovered_tile_id)
