r"""Lists of Art Media from Wikipedia, under the Creative Commons Attribution-ShareAlike License 3.0."""

from .lists import multiline_text_to_list

PAINTING_MATERIALS = multiline_text_to_list("""
Acrylic paint
Chalk
Charcoal
Conté
Crayon
Gouache
Graphite
Ink
Oil paint
Glass paint
Pastel
Pixel
Sketch
Tempera
Watercolor
Glitter
Acrylic paint
Blacklight paint
Encaustic paint
Fresco
Gesso
Glaze
Gouache
Ink
Latex paint
Oil paint
Primer
Ink wash (sumi-e)
""", lambda medium: f"{medium} medium")


SURFACES = multiline_text_to_list("""
Canvas
Card stock
Concrete
Fabric
Glass
Human body
Metal
Paper
Plaster
Scratchboard
Stone
Vellum
Wood
Architectural structures
Canvas
Ceramics
Cloth
Glass
Tattoo
Metal
Paper
Paperboard
Vellum
Wall
Wood
""", lambda surface: f"On {surface}")

TOOLS = multiline_text_to_list("""
Brush
Finger
Pen
Ballpoint pen
Fountain pen
Gel pen
Technical pen
Marker
Pencil
Mechanical pencil
Action painting
Aerosol paint
Airbrush
Batik
Brush
Cloth
Paint roller
Paint pad
Palette knife
Sponge
Pencil
Finger
Aerosol paint
Digital painting
Fresco
Image projector
Mosaic
Pouncing
""", lambda tool: f"Using {tool}")

PRINTING_TECHNIQUES = multiline_text_to_list("""
Aquatint
Collotype
Computer
Dye-sublimation
Inkjet
Laser
Solid ink
Thermal
Embossing
Engraving
Etching
Intaglio
Letterpress
Linocut
Lithography
Mezzotint
Moku hanga
Monotype
Offset
Photographic
Planographic
Printing press
Relief
Linocut
Metalcut
Relief etching
Wood engraving
Woodcut
Screen-printing
Woodblock
""", lambda technique: f"{technique} printing technique")

SCULTPURE_MATERIALS = multiline_text_to_list("""
Bone
Bronze
Gemstones
Glass
Granite
Ice
Ivory
Marble
Plaster
Stone
Wax
Wood
Cement
Ceramics
Metal
Plaster
Plastic
Synthetic resin
Wax
Clay
Papier-mâché
Plaster
polystyrene
Sand
Styrofoam
Beads
Corrugated fiberboard
Cardboard
Edible material
Foil
Found objects
Glue
Adhesives
Paperboard
Textile
Wire
Wood
Acids
Corrosion
Glaze
Polychrome
Wax
""", lambda material: f"Sculpted from {material}")
