r"""List Of Art Movements from Wikipedia under the Creative Commons Attribution-ShareAlike License 3.0.
"""

from .lists import multiline_text_to_list

MOVEMENTS = multiline_text_to_list("""
Afrofuturism
ASCII art
Abstract art
Art Brut
Abstract expressionism
Abstract illusionism
Academic art
Action painting
Aestheticism
Altermodern
American Barbizon school
American impressionism
American realism
American Scene Painting
Analytical art
Antipodeans
Arabesque
Arbeitsrat für Kunst
Art & Language
Art Deco
Art Informel
Art Nouveau
Art photography
Arte Povera
Arts and Crafts movement
Ashcan School
Assemblage
Australian Tonalism
Les Automatistes
Auto-destructive art
Barbizon school
Baroque
Bauhaus
Berlin Secession
Black Arts Movement
Bengal School of Art
Brutalism
Classical Realism
Cloisonnism
COBRA
Color Field
Context art
Computer art
Concrete art
Conceptual art
Constructivism
Crystal Cubism
Cubo-Futurism
Cubism
Cynical realism
Dada
Dansaekhwa
Danube school
Dau-al-Set
De Stijl (also known as Neoplasticism)
Deconstructivism
Digital art
Ecological Art
Environmental art
Modern European ink painting
Excessivism
Expressionism
Fantastic realism
Fauvism
Feminist art
Figurative art
Figuration Libre
Fine Art
Folk art
Fluxus
Funk art
Futurism
Geometric abstract art
Glitch art
Graffiti/Street Art
Gutai group
Gothic art
Happening
Harlem Renaissance
Heidelberg School
Hudson River School
Hurufiyya
Hypermodernism
Hyperrealism
Impressionism
Incoherents
Interactive Art
Institutional critique
International Gothic
International Typographic Style
Kinetic art
Kinetic Pointillism
Kitsch movement
Land art
Les Nabis
Letterism
Light and Space
Lowbrow
Lyco art
Lyrical abstraction
Magic realism
Mail art
Mannerism
Massurrealism
Maximalism
Metaphysical painting
Mingei
Minimalism
Modernism
Modular constructivism
Naive art
Neoclassicism
Neo-Dada
Neo-expressionism
Neo-Fauvism
Neo-figurative
Neogeo (art)
Neoism
Neo-primitivism
Neo-romanticism
Net art
New Objectivity
New Sculpture
Northwest School
Nuclear art
Objective abstraction
Op Art
Orphism
Photorealism
Panfuturism
Paris School
Pixel art
Plasticien
Plein Air
Pointillism
Pop art
Post-impressionism
Postminimalism
Precisionism
Pre-Raphaelitism
Primitivism
Private Press
Process art
Psychedelic art
Purism
Qajar art
Quito School
Rasquache
Rayonism
Realism
Regionalism
Remodernism
Renaissance
Retrofuturism
Rococo
Romanesque
Romanticism
Samikshavad
Serial art
Shin hanga
Shock art
Sōsaku hanga
Socialist realism
Sots art
Space art
Street art
Stuckism
Sumatraism
Superflat
Suprematism
Surrealism
Symbolism
Synchromism
Synthetism
Tachisme (aka Informel)
Temporary art
Toyism
Transgressive art
Tonalism
Ukiyo-e
Underground comix
Unilalianism
Vancouver School
Vanitas
Verdadism
Video art
Visual Art
Viennese Actionism
Vorticism
""", lambda movement: f"{movement} movement")


"""
The MIT License (MIT)

Copyright © 2022 Hex Miller-Bakewell

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
