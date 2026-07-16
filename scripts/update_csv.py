import csv
import sys
import os

# The mapping from the user's request (Common Name | Species)
mapping_text = """Abelia | Abelia
Actaea | Actaea
Adam's Needle | Yucca filamentosa
Aeonium | Aeonium
African Daisy | Osteospermum x hybrida
African Iris | Dietes Iridioides
African Marigold | Tagetes erecta
African Milk Tree | Euphorbia trigona
African Spear Plant | Dracaena angolensis
Agapanthus | Agapanthus
Agastache | Agastache
Agave | Agave
Aglaonema Pictum Tricolor | Aglaonema Pictum Tricolor
Allium | Allium
Almond Tree | Prunus dulcis
Alocasia Azlanii | Alocasia Azlanii
Alocasia Black Velvet | Alocasia Reginula 'Black Velvet'
Alocasia Dragon Scale | Alocasia Baginda 'Dragon Scale'
Alocasia Frydek | Alocasia Micholitziana 'Frydek'
Alocasia Jacklyn | Alocasia Tandurusa 'Jacklyn'
Alocasia Maharani | Alocasia Maharani
Alocasia Melo | Alocasia Melo
Alocasia Odora | Alocasia Odora
Alocasia Pink Dragon | Alocasia Lowii 'Morocco'
Alocasia Polly | Alocasia × amazonica 'Polly'
Alocasia Regal Shield | Alocasia ‘Regal Shield’
Alocasia Sarian | Alocasia 'Sarian'
Alocasia Silver Dragon | Alocasia Baginda 'Silver Dragon'
Alocasia Stingray | Alocasia Macrorrhiza ‘Stingray’
Alocasia Tiny Dancer | Alocasia 'Tiny Dancer'
Alocasia Wentii | Alocasia Wentii
Alocasia Zebrina | Alocasia Zebrina
Alocasia | Alocasia
Aloe Ferox | Aloe Ferox
Aluminum Plant | Pilea Cadierei
Alyssum | Lobularia maritima
Amaranth | Amaranthus
Amaryllis | Hippeastrum
Amber Jubilee Ninebark | Physocarpus opulifolius 'Jefam' AMBER JUBILEE
American Elderberry | Sambucus canadensis
American Ginseng | Panax quinquefolius
American Hornbeam | Carpinus caroliniana
American Sweetgum | Liquidambar styraciflua 'Rotundiloba'
Amur Maple | Acer ginnala
Anaheim Pepper Plant | Capsicum annuum ‘Anaheim’
Anemone | Anemone
Angel's Trumpet | Brugmansia spp.
Angelica | Angelica archangelica
Angelina Stonecrop | Sedum rupestre 'angelina'
Angelonia | Angelonia angustifolia
Anise Hyssop | Agastache foeniculum
Annabelle Hydrangea | Hydrangea arborescens 'Annabelle'
Annual Vinca | Catharanthus roseus
Anthurium Clarinervium | Anthurium Clarinervium
Anthurium Crystallinum | Anthurium Crystallinum
Anthurium Veitchii | Anthurium Veitchii
Anthurium | Anthurium
Apple Mint | Mentha Suaveolens
Arabian Jasmine | Jasminum sambac
Areca Palm | Dypsis lutescens
Arizona Cypress | Cupressus arizonica
Aronia | Aronia melanocarpa
Arrowhead Vine | Syngonium podophyllum
Arrowwood Viburnum | Viburnum dentatum
Artemisia | Artemisia
Artichoke | Cynara scolymus
Arugula | Eruca vesicaria
Asiatic Jasmine | Trachelospermum Asiaticum
Asiatic Lily | Lilium asiatica
Asparagus Fern | Asparagus aethiopicus
Asparagus | Asparagus officinalis
Asplenium Antiquum | Asplenium antiquum
Asters | Symphyotrichum
Astilbe | Astilbe
Aubrieta | Aubrieta
Australian Tree Fern | Cyathea cooperi
Austrian Pine | Pinus nigra
Autograph Tree | Clusia rosea
Autumn Blaze Maple Tree | Acer x freemanii
Autumn Crocus | Colchicum autumnale
Autumn Fern | Dryopteris erythrosora
Autumn Joy Stonecrop | Hylotelephium telephium
Autumn Sage | Salvia greggii
Avocado | Persea americana
Azalea | Rhododendron
Baby Rubber Plant | Peperomia Obtusifolia
Baby Tears | Soleirolia soleirolii
Baby's Breath | Gypsophila
Bacopa | Sutera cordata
Bahia Grass | Paspalum notatum
Ball Cactus | Parodia magnifica
Balloon Flower | Platycodon grandiflorus
Baltic Blue Pothos | Epipremnum Pinnatum 'Baltic Blue'
Bamboo | Bambusa Vulgaris
Banana Yucca | Yucca baccata
Banana | Musa
Bartlett Pear | Pyrus communis
Basil | Ocimum basilicum
Basket Flower | Centaurea americana
Basket Plant | Callisia fragrans
Bat Flower | Tacca chantrieri
Bay Laurel | Laurus nobilis
Bear's Breeches | Acanthus mollis
Bearded Iris | Iris germanica
Beardtongue | Penstemon
Beautyberry | Callicarpa americana
Becky Shasta Daisy | Leucanthemum x superbum 'becky'
Bee Balm | Monarda didyma
Beefsteak Tomato | Solanum lycopersicum 'Beefsteak'
Beet | Beta vulgaris
Begonia Grandis | Begonia grandis
Begonia Maculata | Begonia Maculata
Begonia | Begonia
Bell Pepper | Capsicum annuum
Belladonna | Atropa Belladonna
Bellflower | Campanula
Bells Of Ireland | Moluccella laevis
Bergenia | Bergenia cordifolia or Begenia crassifolia
Bermuda Grass | Cynodon dactylon
Better Boy Tomato | Solanum lycopersicum ‘Better Boy’
Bidens | Bidens
Big Bluestem | Andropogon Gerardii
Bigleaf Hydrangea | Hydrangea macrophylla
Bigleaf Periwinkle | Vinca Major
Bing Cherry Tree | Prunus avium ‘Bing’
Bird Of Paradise | Strelitzia reginae
Bird's Nest Fern | Asplenium nidus
Black Bamboo | Phyllostachys nigra
Black Diamond Watermelon | Citrullus lanatus ‘Black Diamond’
Black Gum Tree | Nyssa sylvatica
Black Hills Spruce | Picea glauca ‘Densata’
Black Krim Tomato | Solanum lycopersicum ‘Black Krim’
Black Lace Elderberry | Sambucus nigra 'eva'
Black Magic Rose | Rosa 'Black Magic'
Black Mondo Grass | Ophiopogon planiscapus 'Nigrescens'
Black-Eyed Susan Vine | Thunbergia alata
Black-Eyed Susan | Rudbeckia hirta
Blackberry Lily | Iris domestica
Blackberry | Rubus fruticosus
Blanket Flower | Gaillardia x grandiflora
Blazing Star | Liatris spicata
Bleeding Heart Indoors | Lamprocapnos spectabilis
Bleeding Heart Vine | Clerodendrum thomsoniae
Bleeding Heart | Lamprocapnos spectabilis
Blood Flower | Asclepias curassavica
Blood Leaf Plant | Iresine herbstii
Blood Lily | Scadoxus multiflorus
Bloodgood' Japanese Maple | Acer palmatum 'bloodgood'
Bloomerang Lilac | Syringa x 'Penda'
Bloomstruck Hydrangea | Hydrangea macrophylla 'P11HM-11'
Blue Atlas Cedar | Cedrus atlantica
Blue Beard | Caryopteris x clandonensi
Blue Eyed Grass | Sisyrinchium angustifolium
Blue Fescue | Festuca glauca
Blue Princess Holly | Ilex x meserveae 'Blue princess'
Blue Rug Juniper | Juniperus horizontalis 'wiltonii'
Blue Spruce | Picea pungens
Blue Spur Flower | Plectranthus barbatus
Blue Star Creeper | Isotoma fluviatilis
Blue Star Fern | Phlebodium aureum
Blue Star Juniper | Juniperus squamata'blue star'
Blueberries | Vaccinium
Bluebonnet | Lupinus x hybrida
Bobo Hydrangea | Hydrangea paniculata 'Ilvobo' BOBO
Bok Choy | Brassica rapa var. chinensis
Bonsai Pine | Pinus bonsai
Borage | Borago officinalis
Boston Fern | Nephrolepsis exalta 'bostoniensis'
Boston Ivy | Parthenocissus tricuspidata
Boxelder | Acer negundo
Boxwood | Buxus
Brass Buttons | Leptinella squalida
Bridal Wreath | Spiraea prunifolia
Broccoli | Brassica oleracea var. italica
Bromeliad | Bromeliaceae genera
Broom | Cytisus and genista
Brunfelsia | Brunfelsia pauciflora
Brussels Sprouts | Brassica oleracea var. gemmifera
Buddha Belly Bamboo | Bambusa Ventricosa
Buffalo Grass | Bouteloua dactyloides
Bugleweed | Ajuga reptans
Bunny Ear Cactus | Opuntia microdasys
Bur Oak | Quercus macrocarpa
Bush Daisy | Euryops pectinatus
Butterfly Bush | Buddleia davidii
Butterfly Pea Plant | Clitoria ternatea
Butterfly Weed | Asclepias tuberosa
Butterhead Lettuce | Latuca sativa var. capitata
Butternut Squash | Cucurbita moschata
Button Fern | Hemionitis rotundifolia
Buttonbush | Cephalanthus occidentalis
Cabbage | Brassica oleracea
Cactus | Cactaceae
Caladium | Caladium
Calathea Beauty Star | Calathea Ornata
Calathea Musaica | Calathea Musaica
Calathea Orbifolia | Calathea Orbifolia
Calathea Ornata | Goeppertia Ornata
Calathea Roseopicta | Calathea Roseopicta
Calathea Warscewiczii | Calathea Warscewiczii
Calathea White Fusion | Calathea lietzei 'White Fusion'
Calathea Zebrina | Calathea Zebrina
Calathea | Calathea spp.
Calendula | Calendula officinalis
Calibrachoa | Calibrachoa group
California Lilac | Ceanothus
California Poppy | Eschscholzia californica
Camellia | Camellia
Camphor | Cinnamomum camphora
Canadian Hemlock Tree | Tsuga canadensis
Candy Corn Plant | Cuphea micropetala
Candy Onion | Amaryllidaceae Allium Cepa
Candytuft | Iberis sempervirens
Canna Lily | Canna x generalis
Canna | Canna spp.
Cantaloupe | Cucumis melo
Canterbury Bells | Campanula medium
Cape Honeysuckle | Tecoma capensis
Cape Plumbago | Plumbago Auriculata
Caper Bush | Capparis spinosa
Cardamom | Elettaria Cardamomum
Cardboard Palm | Zamia furfuracea
Cardinal Climber | Ipomoea multifida
Cardinal Flower | Lobelia cardinalis
Carnations | Dianthus caryophyllus
Carolina Allspice | Calycanthus floridus
Carrot | Daucus carota
Carrotwood Tree | Cupaniopsis anacardioides
Caryopteris | Caryopteris
Cassava | Manihot esculenta
Cast Iron Plant | Aspidistra elatior
Cat Palm | Chamaedorea cataractarum
Cat Whiskers | Orthosiphon aristatus
Catalpa | Catalpa
Catawba Rhododendron | Rhododendron catawbiense
Catmint | Nepeta
Catnip | Nepeta cataria
Cattail | Typha latifolia
Cattleya Orchid | Cattleya spp.
Cauliflower | Brassica oleracea
Cayenne Pepper | Capsicum annuum
Cebu Blue Pothos | Epipremnum pinnatum 'Cebu Blue'
Cedar Of Lebanon | Cedrus libani
Celebrity Tomato | Solanum lycopersicum, cultivar 'Celebrity'
Centipede Grass | Eremochloa ophiuroides
Century Plant | Agave americana
Chamomile | Chamaemelum nobile
Chaste Tree | Vitex Agnus-Castus
Chenille Plant | Acalypha hispida
Cherimoya | Annona cherimola
Cherokee Purple Tomato | Solanum lycopersicum 'Cherokee Purple'
Cherry Laurel | Prunus laurocerasus
Cherry Tomato | Solanum lycopersicum
Cherry Tree Bonsai | Prunus spp.
Chia | Salvia hispanica
Chicago Hardy Fig | Ficus carica ‘Chicago Hardy’
Chickpea Plant | Cicer arietinum
China Aster | Callistephus chinensis
China Doll Plant | Radermachera sinica
Chinese Evergreen | Aglaonema commutatum
Chinese Fan Palm | Livistona chinensis
Chinese Forget-Me-Not | Cynoglossum Amabile
Chinese Fringe Flower | Loropetalum chinense
Chinese Fringe Tree | Chionanthus Retusus
Chinese Holly | Ilex cornuta
Chinese Lantern | Physalis alkekengi
Chinese Money Plant | Pilea peperomioides
Chinese Peony | Paeonia lactiflora
Chinese Pistache | Pistacia chinensis
Chinese Silver Grass | Miscanthus sinensis
Chinese Snowball | Viburnum macrocephalum
Chinkapin Oak | Quercus muehlenbergii
Chives | Allium schoenoprasum
Chocolate Cosmos | Cosmos atrosanguineus
Chocolate Mint | Mentha x piperita 'chocolate'
Chocolate Soldier Plant | Kalanchoe tomentosa
Chocolate Vine | Akebia quinata
Chokecherry | Prunus virginiana
Christmas Cactus | Schlumbergera x buckleyi
Christmas Rose | Helleborus niger
Chrysanthemum | Chrysanthemum morifolium
Cilantro | Coriandrum sativum
Cineraria | Pericallis cruenta
Cinnamon Basil | Ocimum Basilicum ‘Cinnamon’
Cinnamon | Cinnamomum
Cissus Discolor | Cissus discolor
Citronella Plant | Cymbopogon nardus
Clematis | Clematis spp.
Cleome | Cleome spp.
Climbing Aloe | Aloiampelos ciliaris
Climbing Hydrangea | Hydrangea anomala
Clove | Syzygium aromaticum
Cockscomb | Celosia argentea var. cristata
Coconut Orchid | Maxillaria Tenuifolia
Coconut Palm | Cocos nucifera
Coffee Plant | Coffea arabica
Coleus | Plectranthus scutellarioides
Collard Greens | Brassica oleracea
Columbine | Aquilegia
Comfrey | Symphytum officinale
Common Juniper | Juniperus communis
Common Tansy | Tanacetum vulgare
Contorted Filbert | Corylus avellana 'contorta'
Coral Bark Maple | Acer palmatum 'Sango-Kaku'
Coral Bells | Heuchera
Coral Cactus | Euphorbia lactea ‘Cristata’
Coral Honeysuckle | Lonicera sempervirens
Cordyline | Cordyline terminalis
Coreopsis | Coreopsis spp.
Corkscrew Willow | Salix matsudana 'tortuosa'
Corn Plant | Dracaena fragrans
Cornflower | Centaurea cyanus
Corsican Mint | Mentha requienii
Cosmos | Cosmos sulphureus
Cotton Rose | Hibiscus mutabilis
Cowslip | Primula Veris
Crassula | Crassula spp.
Creeping Bellflower | Campanula rapunculoides
Creeping Jenny | Lysimachia nummularia
Creeping Juniper | Juniperus horizontalis
Creeping Mazus | Mazus reptans
Creeping Phlox | Phlox stolonifera
Creeping Speedwell | Veronica filiformis
Creeping Thyme | Thymus
Creeping Wire Vine | Muehlenbeckia axillaris
Crepe Myrtle | Lagerstroemia indica
Crimson King Norway Maple | Acer platanoides ‘Crimson King’
Crimson Queen Japanese Maple Tree | Acer palmatum
Crinum Lily | Crinum Asiaticum
Crocodile Fern | Microsorum Musifolium
Crocosmia | Crocosmia spp.
Crocus | Crocus
Crossandra | Crossandra infundibuliformis
Croton | Codiaeum variegatum
Crown Imperial | Fritillaria imperialis
Cryptanthus | Cryptanthus
Cucuzza Squash | Lagenaria siceraria
Cup And Saucer Vine | Cobaea scandens
Cup Plant | Silphium perfoliatum
Cuphea | Cuphea Spp.
Curry Plant | Murraya koenigii
Cyclamen Persicum | Cyclamen persicum
Cyclamen | Cyclamen persicum
Cymbidium Orchid | Cymbidium
Cypress Vine | Ipomoea quamoclit
Daffodil | Narcissus
Dahlia | Dahlia
Daphne | Daphne
Date Palm | Phoenix dactylifera
Dawn Redwood | Metasequoia glyptostroboides
Daylily | Hemerocallis
Delphinium | Delphinium
Dendrobium Orchid | Dendrobium
Deodar Cedar | Cedrus deodara
Desert Rose | Adenium obesum
Desert Spoon | Dasylirion wheeleri
Desert Willow | Chilopsis linearis
Devil's Backbone | Euphorbia tithymaloides
Dianthus | Dianthus spp.
Dieffenbachia Seguine | Dieffenbachia seguine
Dieffenbachia | Dieffenbachia
Dinner Plate Dahlia | Dahlia spp.
Dog Tail Cactus | Strophocactus testudo
Domino Variegated Peace Lily | Spathiphyllum wallisii 'Domino'
Donkey's Tail | Sedum morganianum
Doublefile Viburnum | Viburnum plicatum
Dracaena Janet Craig | Dracaena fragrans 'Compacta'
Dracaena | Dracaena
Dracula Orchid | Dracula spp.
Dragon Lily | Dracunculus vulgaris
Dragon Plant | Dracaena marginata
Dragon Tree | Dracaena draco
Dragonfruit | Selenicereus undatas
Duckweed | Lemna minor
Duranta | Duranta erecta
Dusty Miller | Jacobaea maritima
Dutchman's Pipe Vine | Aristolochia macrophylla
Dwarf Alberta Spruce | Picea glauca 'Conica'
Dwarf Jade | Portulacaria afra
Dwarf Mondo Grass | Ophiopogon japonicus 'Nana'
Dwarf Morning Glory | Evolvulus glomeratus
Dwarf Mugo Pine | Pinus mugo
Dymondia | Dymondia margaretae
Early Girl Tomato | Solanum lycopersicum ‘Early Girl’
Easter Cactus | Rhapsalideae gaertneri
Easter Lily | Lilium longiflorum
Eastern Prickly Pear Cactus | Opuntia humifusa
Eastern Red Cedar | Juniperus virginiana
Eastern White Pine | Pinus strobus
Echeveria | Echeveria
Echinocereus | Echinocereus spp.
Edamame Plant | Glycine max
Edelweiss | Leontopodium alpinum
Elatior Begonia | Begonia x hiemalis
Elephant Ear Plant | Colocasia
Emerald Gaiety Wintercreeper | Euonymus fortunei 'Emerald Gaiety'
Emerald Green Arborvitae | Thuja occidentalis
Endless Summer Hydrangea | Hydrangea macrophylla 'endless summer'
English Bluebells | Hyacinthoides non-scripta
English Daisy | Bellis perennis
English Ivy | Hedera helix
English Lavender | Lavandula angustifolia
English Walnut | Juglans regia
Epimedium | Epimedium
Epipremnum Pinnatum | Epipremnum pinnatum
Eucalyptus | Eucalyptus cinerea
Euphorbia Ingens | Euphorbia ingens
Euphorbia | Euphorbia
Eureka Lemon Tree | Citrus x limon 'eureka'
European Beech | Fagus sylvatica
European Fan Palm | Chamaerops humilis
European Mountain Ash | Sorbus aucuparia
Evening Primrose | Oenothera biennis
Everbearing Strawberries | Fragaria × Ananassa 'Quinault'
Fall Fiesta Sugar Maple | Acer saccharum 'Bailsta' FALL FIESTA
False Aralia | Plerandra elegantissima
False Holly | Osmanthus fragrans
False Indigo | Baptisia australis
False Sunflower | Heliopsis helianthoides
Fan Flower | Scaevola aemula
Fatsia Spider Web | Fatsia japonica ‘Spider Web’
Fava Bean | Vicia faba
Feather Reed Grass | Calamagrostis x acutiflora
Ficus Audrey | Ficus benghalensis
Ficus Ruby | Ficus elastica 'Ruby'
Ficus Shivereana | Ficus elastica 'Shivereana'
Ficus Tineke | Ficus elastica 'tineke'
Ficus Tree | Ficus benjamina
Ficus Umbellata | Ficus umbellata
Fiddle-Leaf Fig | Ficus lyrata
Fire Lily | Clivia miniata
Firebush | Hamelia patens
Firepower Nandina | Nandina domestica 'firepower'
Firespike | Odontonema strictum
Fishbone Cactus | Disocactus anguliger
Fishtail Palm | Caryota
Flame Azalea | Rhododendron calendulaceum
Flame Tree | Delonix regia
Flamingo Willow | Salix integra 'flamingo'
Flapjack Plant | Kalanchoe luciae
Flax Lily | Dianella tasmanica
Flax | Linum usitatissimum
Floribunda Rose | Polyantha Rose x Hybrid Teas
Florida Beauty | Dracaena Surculosa 'Florida Beauty'
Flower of Bristol | Lychnis chalcedonica
Flowering Almond | Prunus glandulosa
Flowering Crabapple | Malus rosaceae
Flowering Ginger | Zingiberaceae
Flowering Quince | Chaenomeles speciosa
Flowering Tobacco | Nicotiana alata
Foamflower | Tiarella cordifolia
Forest Pansy Redbud | Cercis canadensis 'Forest Pansy'
Forget-Me-Not | Myosotis sylvatica
Forsythia | Forsythia
Four O'Clock Plant | Mirabilis jalapa
Foxtail Fern | Asparagus densiflorus
Foxtail Palm | Wodyetia bifurcata
Fraser Fir | Abies Fraseri
Freesia | Freesia
French Lavender | Lavandula dentata
French Marigold | Tagetes patula
Frizzle Sizzle | Albuca spiralis
Frog Fruit | Phyla nodiflora
Fuschia | Fuschia
Garden Phlox | Phlox paniculata
Gardenia | Gardenia jasminoides
Garlic | Allium Sativum
Gas Plant | Dictamnus albus
Gasteria | Gasteria
Gaura | Oenothera Lindheimeri
Gazania | Gazania rigens
Geranium | Pelargonium spp.
Gerber | Gerbera jamesonii
Ghost Plant | Graptopetalum paraguayense
Ginkgo Biloba Tree | Gingko biloba
Glacier Pothos | Epipremnum aureum 'Glacier'
Globe Amaranth | Gomphrena
Globe Thistle | Echinops
Gloriosa Lily | Gloriosa superba
Glory of the Snow | Chionodoxa luciliae
Gloxinia | Sinningia speciosa
Goatsbeard | Aruncus dioicus
Gold Dust | Aucuba japonica
Gold Mound Spirea | Spiraea japonica 'Gold mound'
Golden Alexander | Zizia aurea
Golden Bamboo Indoors | Phyllostachys aurea
Golden Bamboo | Phyllostachys aurea
Golden Barberry | Berberis thunbergii 'aurea'
Golden Barrel Cactus | Echinocactus grusonii
Golden Chain Tree | Laburnum
Goldenrod | Solidago
Goldfish Plant | Nematanthus gregarious
Goldflame Honeysuckle | Lonicera x heckrottii
Goldflame Spirea | Spiraea japonica 'goldflame'
Gollum Jade | Crassula ovata 'Gollum'
Gooseberry | Ribes uva-crispa
Grape Hyacinth | Muscari armeniacum
Grape Vine | Vitis Vinifera
Gray Birch | Betula populifolia
Green Giant Arborvitae | Thuja standishii x plicata ‘Green Giant’
Grevillea | Grevillea
Ground Cherry | Physalis pruinosa
Halcyon Hosta | Hosta 'Halcyon'
Hardy Geranium | Geranium spp.
Hardy Hibiscus | Hibiscus moscheutos
Hardy Kiwi | Actinidia arguta
Hardy Mum | Chrysanthemum morifolium
Hass Avocado Tree | Persea americana 'Hass'
Hawaiian Pothos | Epipremnum aureum 'Hawaiian'
Haworthia Cooperi | Haworthia Cooperi
Haworthia | Haworthia
Hawthorn | Crataegus
Hazelnut Tree | Corylus avellana
Heartleaf Philodendron | Philodendron scandens
Heather | Calluna vulgaris
Heavenly Bamboo | Nandina domestica
Hebe Shrub | Hebe
Helenium | Helenium autumnale
Heliconia Rostrata | Heliconia rostrata
Heliconia | Heliconia
Heliotrope | Heliotropium
Hellebore | Helleborus
Hens And Chicks | Sempervivum tectorum
Hibiscus | Hibiscus
Hickory Tree | Carya spp.
Himalayan Birch | Betula utilis
Hindu Rope Plant | Hoya carnosa 'compacta'
Hinoki Cypress | Chamaecyparis obtusa
Hollyhock | Alcea Spp.
Holy Basil | Ocimum tenuiflorum
Honeysuckle | Lonicera spp.
Hong Kong Orchid Tree | Bauhinia × blakeana
Hoptree | Ptelea trifoliata
Horseradish | Armoracia rusticana
Horsetail | Equisetum hyemale
Hosta | Hosta spp.
Hoya 'Krimson Queen' | Hoya carnosa 'Krimson Queen'
Hoya Australis | Hoya australis
Hoya Kentiana | Hoya Kentiana
Hoya Kerrii | Hoya kerrii
Hoya Obovata | Hoya obovata
Hoya Rosita | Hoya wayetii x tsangii
Hoya Shepherdii | Hoya shepherdii
Hoya Sunrise | Hoya lacunosa x obscura 'Sunrise'
Hoya Wayetii | Hoya Wayetii
Huernia Zebrina | Huernia zebrina
Hummingbird Bush | Anisacanthus quadrifidus var. wrightii
Hyacinth | Hyacinthus orientalis
Hybrid Tea Roses | Rosa x hybrida
Hydrangea Serrata | Hydrangea Serrata
Hydrangea | Hydrangea
Ice Plant | Delosperma
Iceland Poppy | Papaver nudicaule
Impatiens | Impatiens
Inaba Shidare Japanese Maple | Acer palmatum 'Inaba Shidare'
Inch Plant | Tradescantia zebrina
Incrediball Hydrangea | Hydrangea arborescens 'Abetwo' INCREDIBALL
Indian Hawthorn | Rhaphiolepis indica
Inkberry Holly | Ilex glabra
Irish Moss | Sagina subulata
Italian Cypress | Cupressus sempervirens
Itoh Peony | Paeoniaceae
Ivory Halo Dogwood | Cornus alba 'Bailhalo'
Ivory Silk Lilac | Syringa reticulata 'Ivory Silk'
Ivy Geranium | Pelargonium peltatum
Jacaranda Tree | Jacaranda mimosifoila
Jack-in-the-Pulpit | Arisaema triphyllum
Jackfruit | Artocarpus heterophyllus
Jackman Clematis | Clematis 'jackmanii'
Jacob's Ladder | Polemonium caeruleum
Jade Plant | Crassula ovata
Jade Pothos | Epipremnum aureum 'Jade'
Jalapeño Pepper | Capiscum annuum 'jalapeño'
Jane Magnolia | Magnolia 'Jane'
Japanese Andromeda | Pieris japonica
Japanese Anemone | Eriocapitella x hybrida
Japanese Aralia | Fatsia japonica
Japanese Barberry | Berberis thunbergii
Japanese Black Pine | Pinus thunbergii
Japanese Blood Grass | Imperata cylindrica
Japanese Camellia | Camellia Japonica
Japanese Fern Tree | Filicium decipiens
Japanese Flag | Iris ensata
Japanese Flowering Cherry | Prunus serrulata
Japanese Forest Grass | Hakonechloa macraaureola
Japanese Holly | Ilex crenata
Japanese Honeysuckle | Lonicera japonica
Japanese Lilac Tree | Syringa reticulata
Japanese Maple Bonsai | Acer palmatum bonsai
Japanese Maple | Acer palmatum
Japanese Pagoda | Styphnolobium japonicum
Japanese Painted Fern | Athyrium nipponicum
Japanese Pieris | Pieris japonica
Japanese Rose | Kerria japanica
Japanese Sedge | Carex morrowii
Japanese Snowbell | Styrax japonicus
Japanese Stewartia | Stewartia pseudocamellia
Jasmine Indoors | Jasminus spp.
Jasmine | Jasminum
Jessenia Pothos | Epipremnum aureum 'Jessenia'
Jewel Orchid | Ludisia discolor
Jewelweed | Impatiens capensis
Joe Pye Weed | Eutrochium purpureum
Joseph's Coat | Alternanthera
Joshua Tree | Yucca Brevifolia
Juniper Bonsai | Juniperus bonsai
Kalanchoe Delagoensis | Kalanchoe Delagoensis
Kalanchoe Fedtschenkoi | Bryophyllum fedtschenkoi
Kalanchoe Pinnata | Kalanchoe pinnata
Kalanchoe Thyrsiflora | Kalanchoe thyrsiflora
Kalanchoe | Kalanchoe blossfeldiana
Kale | Brassica oleracea
Kangaroo Paw | Anigozanthos
Karl Foerster Feather Reed Grass | Calamagrostis x acutifolia 'Karl Foerster'
Katsura Tree | Cercidiphyllum japonicum
Kentia Palm | Howea forsteriana
Kentucky Bluegrass | Poa pratensis
Kentucky Coffee Tree | Gymnocladus dioicus
Kimberley Queen Fern | Nephrolepis obliterata
Knock Out Rose | Rosa hybrida
Kohuhu | Pittosporum tenuifolium
Korean Fir | Abies koreana
Korean Spicebush | Viburnum carlesii
Krantz Aloe | Aloe arborescens
Kudzu | Pueraria montana
Kumquat | Citrus japonica
Lace Aloe | Aristaloe aristata
Lacecap Hydrangea | Hydrangea macrophylla
Lady Fern | Athyrium filix-femina
Lady Palm | Rhapis excelsa
Lady Slipper Orchid | Cypripedium spp.
Lady's Mantle | Alchemilla mollis
Lamb's Ear | Stachys byzantina
Lantana | Lantana camara
Larkspur | Delphinium
Lavatera | Lavatera spp.
Lavender Cotton | Santolina chamaecyparissus
Lavender Indoors | Lavandula spp.
Lavender | Lavandula
Lemon Balm | Melissa officinalis
Lemon Button Fern | Nephrolepis cordifolia 'Duffii'
Lemon Cucumber | Cucumis sativus 'Lemon'
Lemon Cypress | Cupressus macrocarpa 'goldcrest'
Lemon Lime Dracaena | Dracaena fragrans ‘Lemon Lime’
Lemon Lime Maranta | Maranta leuconeura 'Lemon Lime'
Lemon Meringue Pothos | Epipremnum aureum 'Lemon Meringue'
Lemon Tree | Citrus limon
Lemon Verbena | Aloysia citriodora
Lemongrass | Cymbopogon citratus
Lenten Rose | Helleborus x hybridus
Lentil | Lens culinaris
Leopard Plant | Farfugium japonicum
Lettuce | Lactuca sativa
Leucadendron | Leucadendron
Leyland Cypress | Cuprocyparis leylandii
Licorice Plant | Helichrysum petiolare
Licuala Grandis | Licuala grandis
Ligularia | Ligularia
Lilac Bush | Syringa vulgaris
Lima Bean | Phaseolus lunatus
Lime Tree | Citrus × latifolia
Limelight Hydrangea | Hydrangea paniculata 'Limelight'
Lion's Tail | Leonotis Leonurus
Lipstick Palm | Cyrtostachys renda
Lipstick Plant | Aeschynanthus radicans
Liriope | Liriope spicata
Lisianthus | Eustoma grandiflorum
Lithodora | Lithodora diffusa
Little Bluestem | Schizachyrium scoparium
Little Gem Magnolia Tree | Magnolia grandiflora 'Little Gem'
Little Princess Spirea | Spiraea japonica 'Little Princess'
Little-Leaf Linden | Tilia cordata
Living Stone | Lithops
Lobelia | Lobelia erinus
Loblolly Pine | Pinus taeda
Lombardy Poplar | Populus nigra 'italica'
London Planetree | Platanus x acerifolia
Longevity Spinach | Gynura procumbens
Longleaf Pine | Pinus palustris
Loquat | Eriobotrya japonica
Lotus | Nelumbo spp.
Love-in-a-Mist | Nigella damascena
Love-Lies-Bleeding | Amaranthus caudatus
Lucky Bamboo | Dracaena sanderiana
Luffa | Luffa aegyptiaca
Lungwort | Pulmonaria
Lychee | Litchi chinensis
'Miss Kim' Lilac | Syringa pubescens subsp. patula 'Miss Kim'
Macadamia Nut Tree | Macadamia spp.
Mache | Valerianella locusta
Macho Fern | Nephrolepis biserrata
Madagascar Palm | Pachypodium lamerei
Magnolia Ann | Magnolia liliflora x 'Ann'
Magnolia Grandiflora | Magnolia grandiflora
Mahonia | Mahonia
Maidenhair Fern | Adiantum raddianum
Majesty Palm | Ravenea revularis
Malabar Spinach | Basella alba
Mammillaria Cactus | Mammillaria spp.
Mandevilla | Mandevilla
Mango Tree | Mangifera indica
Manjula Pothos | Epipremnum aureum ‘Manjula’
Marble Queen Pothos | Epipremnum aureum 'Marble Queen'
Marguerite Daisy | Argyranthemum frutescens
Marigold | Tagetes
Marsh Mallow | Althaea officinalis
Mastic Tree | Pistacia lentiscus
Matilja Poppy | Romneya coulteri
May Night Salvia | Salvia sylvestris
Mayapple | Podophyllum peltatum
Meadow Rue | Thalictrum rochebrunianum
Melampodium | Melampodium spp.
Mesclun | Various
Mexican Bird of Paradise | Caesalpinia mexicana
Mexican Bush Sage | Salvia leucantha
Mexican Fan Palm | Washingtonia robusta
Mexican Feather Grass | Nassella tenuissima
Mexican Hat | Ratibida columnifera
Mexican Heather | Cuphea hyssopifolia
Mexican Orange Plant | Choisya ternata
Mexican Petunia | Ruellia brittoniana
Mexican Sunflower | Tithonia rotundifolia
Meyer Lemon Tree | Citrus x meyeri
Milk Thistle | Silybum marianum
Milkweed | Asclepias syriaca
Millet | Pennisetum glaucum
Million Bells | Calibrachoa
Miltonia Orchid | Miltonia
Ming Aralia | Polyscias fruticosa
Mini Monstera | Rhaphidophora Tetrasperma
Miniature Rose | Rosa
Mint | Mentha
Miscanthus | Miscanthus spp.
Mistletoe Cactus | Rhipsalis baccifera
Mistletoe | Phoradendron spp.
Mock Orange Bush | Philadelphus coronarius
Mona Lavender | Plectranthus mona lavender
Money Tree | Pachira aquatica
Monkey Flowers | Mimulus spp.
Monkey Puzzle Tree | Araucaria araucana
Monkey Tail Plant | Cleistocactus Colademononis
Monkshood | Aconitum napellus
Monstera Acacoyaguensis | Monstera acacoyaguensis
Monstera Adansonii Variegated | Monstera adansonii 'Variegata'
Monstera Albo | Monstera deliciosa ‘Albo Borsigiana’
Monstera Deliciosa | Monstera deliciosa
Monstera Dubia | Monstera dubia
Monstera Esqueleto | Monstera Esqueleto
Monstera Lechleriana | Monstera lechleriana
Monstera Obliqua | Monstera Obliqua
Monstera Peru | Monstera karstenianum
Monstera Pinnatipartita | Monstera Pinnatipartita
Monstera Siltepecana | Monstera siltepecana
Monstera Standleyana Albo | Monstera standleyana 'Albo Variegata'
Monstera Thai Constellation | Monstera deliciosa 'Thai Constellation'
Moon Cactus | Gymnocalycium mihanovichii
Moonflower | Ipomoea alba
Moonshine Snake Plant | Dracaena trifasciata ‘Moonshine’
Morel Mushrooms | Morchella
Moringa Tree | Moringa oleifera
Morning Glory | Ipomoea purpurea
Mortgage Lifter Tomato | Solanum lycopersicum 'Mortgage Lifter'
Moss Rose | Portulaca grandiflora
Mother Of Thousands | Kalanchoe daigremontiana
Mountain Laurel | Kalmia latifolia
Mugwort | Artemisia vulgaris
Mulberry | Morus
Mullein | Verbascum thapsus
Mum | Chrysanthemum
Munstead Lavender | Lavandua angustifolia 'munstead'
Mustard Plant | Brassica spp.
Myrtle | Myrtus communis
N'Joy Pothos | Epipremnum aureum 'n'joy'
Nanking Cherry | Prunus tomentosa
Nasturtium | Tropaeolum
Natal Plum | Carissa macrocarpa
Nemesia | Scrophulariaceae
Neon Pothos | Epipremnum aureum 'Neon'
Neoregelia Bromeliad | Neoregelia
Nerve Plant | Fittonia albivenis
Never Never Plant 'Grey Star' | Ctenanthe setosa 'grey star'
Never Never Plant | Ctenanthe spp.
New England Aster | Symphyotrichum novae-angliae
New Guinea Impatiens | Impatiens hawkeri
New York Ironweed | Vernonia noveboracensis
New Zealand Flax | Phormium tenax
New Zealand Tea Tree | Leptospermum scoparium
Night-Blooming Jasmine | Cestrum Nocturnum
Ninebark | Physocarpus opulifolius
Nippon Daisy | Nipponanthemum nipponicum
Norfolk Island Pine | Araucaria heterophylla
Northern Bush Honeysuckle | Diervilla lonicera
Norway Spruce | Picea abies
Nova Zembla Rhododendron | Rhododendron x 'Nova Zembla'
Nutmeg Tree | Myristica fragrans
Oakleaf Hydrangea | Hydrangea quercifolia
October Glory Maple | Acer rubrum 'October Glory'
Okra | Abelmoschus esculentus
Oleander | Nerium oleander
Onion | Allium cepa
Orange Daylily | Hemerocallis fulva
Orange Jasmine | Murraya paniculata
Orange Lily | Lilium bulbiferum
Orange Tree | Citrus sinensis
Orchid Cactus | Epiphyllum
Oregano | Origanum spp.
Oriental Bittersweet | Celastrus orbiculatus
Oriental Poppy | Papaver orientale
Ornamental Cabbage | Brassica oleracea
Ornamental Pepper | Capsicum annuum cultivars
Osakazuki Japanese Maple | Acer palmatum 'Osakazuki
Osiria Rose | Rosa 'Osiria'
Ostrich Fern | Matteuccia struthiopteris
Oxalis | Oxalis
Oxeye Daisy | Leucanthemum vulgare
Pagoda Dogwood | Cornus alternifolia
Painted Daisy | Tanacetum coccineum
Painted Lady Philodendron | Philodendron erubescens 'Painted Lady'
Palm Tree | Arecaceae family
Pampas Grass | Cortadelia selloana
Pansy | Viola x wittrockiana
Papaya | Carica papaya
Paper Birch | Betula papyrifera
Paperbark Maple | Acer griseum
Paperwhite Narcissus | Narcissus papyraceus
Paphiopedilum Orchid | Paphiopedilum
Papyrus | Cyperus papyrus
Parlor Palm | Chamaedorea elegans
Parsley | Petroselinum crispum
Passionflower | Passiflora
Pattypan Squash | Cucurbita pepo
Pawpaw | Asimina triloba
Peace Lily | Spathiphyllum
Peace Rose | Rosa ‘Madame A. Meilland’
Peach | Prunus persica
Peacock Plant | Calathea makoyana
Peanut Butter Bush | Clerodendrum trichotomum
Peanuts | Arachis hypogaea
Pearls and Jade Pothos | Epipremnum aureum 'Pearls and Jade'
Pencil Cactus | Euphorbia tirucalli
Pennisetum (Fountain Grass) | Pennisetum
Penny Mac Hydrangea | Hydrangea macrophylla 'Penny Mac'
Pennyroyal | Mentha pulegium
Peony | Paeonia
Peperomia Caperata | Peperomia caperata
Peperomia Ginny | Peperomia clusiifolia 'Ginny'
Peperomia Hope | Peperomia tetraphylla
Peperomia Pixie Lime | Peperomia Orba
Peperomia Rosso | Peperomia caperata 'Rosso'
Peperomia Rotundifolia | Peperomia Rotundifolia
Peperomia | Peperomia
Peppercorn Plant | Piper nigrum
Peppermint | Mentha × piperita
Persian Buttercup | Ranunculus asiaticus
Persian Shield | Strobilanthes dyerianus
Persian Silk Tree | Albizia julibrissin
Persian Violet | Exacum affine
Peruvian Lily | Alstroemeria
Petunia | Petunia
Phalaenopsis Orchid | Phalaenopsis
Philodendron Billietiae | Philodendron Billietiae
Philodendron Birkin | Philodendron Birkin
Philodendron Black Cardinal | Philodendron Erubescens 'Black Cardinal'
Philodendron Brandtianum | Philodendron Brandtianum
Philodendron Brasil | Philodendron hederaceum ‘Brasil’
Philodendron Burle Marx | Philodendron burle marxii
Philodendron Dark Lord | Philodendron erubescens ‘Dark Lord’
Philodendron Erubescens | Philodendron erubescens
Philodendron Florida Beauty | Philodendron 'Florida Beauty'
Philodendron Florida Ghost | Squamiferum x Pedatum 'Florida Ghost'
Philodendron Florida Green | Squamiferum x Pedatum 'Florida Green'
Philodendron Gloriosum | Philodendron Gloriosum
Philodendron Imperial Green | Philodendron erubescens ‘Imperial Green’
Philodendron Imperial Red | Philodendron erubescens 'Imperial Red'
Philodendron Mamei | Philodendron mamei
Philodendron Mayoi | Philodendron Mayoi
Philodendron Melanochrysum | Philodendron melanochrysum
Philodendron Micans | Philodendron Micans
Philodendron Moonlight | Philodendron erubescens 'Moonlight'
Philodendron Paraiso Verde | Philodendron Paraiso Verde
Philodendron Pink Princess | Philodendron erubescens 'Pink Princess'
Philodendron Plowmanii | Philodendron plowmanii
Philodendron Prince of Orange | Philodendron 'Prince of Orange'
Philodendron Ring of Fire | Philodendron bipinnatifidum x selloum
Philodendron Rio | Philodendron hederaceum 'Rio'
Philodendron Rojo Congo | Philodendron tatei ‘Rojo Congo’
Philodendron Rugosum | Philodendron Rugosum
Philodendron Silver Sword | Philodendron hastatum ‘Silver Sword’
Philodendron Spiritus-Sancti | Philodendron spiritus-sancti
Philodendron Splendid | Philodendron melanochrysum x verrucosum
Philodendron Squamiferum | Philodendron Squamiferum
Philodendron Verrucosum | Philodendron Verrucosum
Philodendron White Princess | Philodendron eurbensce 'White Princess'
Philodendron Xanadu | Thaumatophyllum xanadu
Philodendron | Philodendron
Phlox | Phlox
Pilea Glauca | Pilea glauca
Pilea Involucrata | Pilea Involucrata
Pilea Microphylla | Pilea Microphylla
Pineapple Guava | Acca sellowiana
Pineapple Lily | Eucomis
Pineapple Sage | Salvia elegans
Pineapple Tomato | Solanum lycopersicum 'Pineapple'
Pineapple | Ananas Comosus
Pink Brandywine Tomato | Solanum lycopersicum 'Brandywine'
Pink Dogwood | Cornus florida
Pink Evening Primrose | Oenothera speciosa
Pink Lemonade Blueberry Bush | Vaccinium 'Pink Lemonade'
Pink Muhly Grass | Muhlenbergia capillaris
Pinto Beans | Phaseolus Vulgaris
Pistachio Tree | Pistaciavera
Pitcher Plant | Nepenthes spp.
Plectranthus | Plectranthus
Plum Blossom Tree | Prunus mume
Plumeria | Plumeria spp.
Podocarpus | Podocarpus
Poinsettia | Euphorbia pulcherrima
Poison Hemlock | Conium maculatum
Pokeweed | Phytolacca americana
Polka Dot Plant | Hypoestes phyllostachya
Ponderosa Pine | Pinus ponderosa
Ponytail Palm | Beaucarnea recurvata
Pop Star® Hydrangea | Hydrangea macrophylla 'Bailmacsix' PP33, 703
Popcorn Plant | Senna didymobotrya
Poppy | Papaver rhoeas
Portulaca | Portulaca
Potato | Solanum tuberosum
Pothos | Epipremnum aureum
Prairie Dropseed | Sporobolus heterolepis
Prairie Smoke | Geum triflorum
Prayer Plant | Maranta leuconeura
Prickly Pear | Opuntia spp.
Pride Of Madeira | Echium candicans
Primrose | Primula spp.
Princess Flower | Tibouchina urvilleana
Privet | Ligustrum
Protea | Protea
Ptilotus | Ptilotus exaltatus
Pumpkin On A Stick | Solanum Integrifolium
Pumpkin | Curbita
Purple Basil | Ocimum basilicum var. purpurascens
Purple Fountain Grass | Pennisetum setaceum 'rubrum'
Purple Heart Plant | Tradescantia Pallida
Purple Hyacinth Bean | Lablab purpureus
Purple Leaf Sand Cherry | Prunus x cistena
Purple Passion Plant | Gynura aurantiaca
Purple Passionflower | Passiflora Incarnata
Purple Shamrock | Oxalis triangularis
Purpleleaf Plum Tree | Prunus cerasifera
Pussy Willow | Salix spp.
Quaking Aspen | Populus tremuloides
Queen Anne's Lace | Daucus carota
Queen Elizabeth Rose | Rosa ‘Queen Elizabeth’
Quick Fire Hydrangea | Hydrangea paniculata ‘Bulk’
Quinoa | Chenopodium quinoa
Radish | Raphanus sativus
Rain Lily | Zephyranthes candida
Rainbow Elephant Bush | Portulacaria afra 'Variegata'
Rambutan | Nephelium lappaceum
Ramps | Allium tricoccum
Ranunculus | Ranunculus spp.
Raspberry Bush | Rubus idaeus
Rat Tail Cactus | Aporocactus flagelliformis
Rattlesnake Plants | Goeppertia insignis
Raven ZZ | Zamioculcas zamiifolia ‘Raven’
Red Button Ginger | Costus Woodsonii
Red Currant | Ribes rubrum
Red Dragon Japanese Maple | Acer palmatum 'Red Dragon'
Red Flowering Currant | Ribes sanguineum
Red Hot Poker | Kniphofia
Red Maple | Acer rubrum
Red Mulberry | Morus Rubra
Red Oak | Quercus rubra
Red Onion | Allium cepa
Red Spider Lily | Lycoris radiata
Red Sunset Maple | Acer rubrum 'franksred'
Red Tip Photinia | Photinia x fraseri
Red-Twig Dogwood | Cornus servicea
Resurrection Lily | Lycoris squamigera
Resurrection Plant | Selaginella lepidophylla
Rex Begonia | Begonia rex-cultorum
Rhaphidophora Decursiva | Rhaphidophora decursiva
Rhipsalis Cactus | Rhipsalis spp.
Rhododendron English Roseum | Rhododendron x 'English Roseum'
Rhododendron Maximum | Rhododendron maximum
Rhododendron | Rhododendron
Rhubarb | Rheum rhabarbarum
River Birch | Betula nigra
Robellini Palm | Phoenix roebelenii
Rock Cress | Aubrieta deltoidea
Rockrose | Cistus
Rockspray Cotoneaster | Cotoneaster horizontalis
Roma Tomato | Solanum lycopersicum 'Roma'
Romaine Lettuce | Lactuca sativa L. var. longifolia
Root Beer Plant | Piper auritum
Rose Campion | Lychnis coronaria
Rose of Sharon | Hibiscus syriacus
Rose | Rosa
Rosemary | Salvia rosmarinus
Rubber Plant | Ficus elastica
Rue | Ruta graveolens
Rugosa Rose | Rosa rugosa
Rupturewort | Herniaria glabra
Ruscus | Ruscus
Russian Sage | Perovskia atriplicifolia
Sago Palm | Cycas revoluta
San Marzano Tomato | Lycopersicon esculentum 'San Marzano'
Saskatoon Serviceberry | Amelanchier alnifolia
Sassafras | Sassafras albium
Satin Pothos | Scindapsus pictus
Satsuma Mandarin | Citrus unshiu
Saucer Magnolia | Magnolia x soulangiana
Scabiosa | Scabiosa
Scallion | Allium fistulosum
Scented-Leaved Geraniums | Pelargonium
Schefflera | Schefflera
Scindapsus Pictus Exotica | Scindapsus Pictus ‘Exotica’
Scotch Pine | Pinus sylvestris
Scottish Moss | Arenaria verna
Sea Holly | Eryngium planum
Sea Lavender | Limonium latifolium
Sedum | Sedum
Selaginella Kraussiana | Selaginella kraussiana
Sensitive Plant | Mimosa pudica
Serrano Pepper | Capsicum annuum
Sesame | Sesamum indicum
Shallot | Allium ascalonium
Shasta Daisy | Leucanthemum x superbum
Shishito Pepper | Capsicum annuum var. grossum
Shrimp Plant | Justicia Brandegeana
Siberian Bugloss | Brunnera macrophylla
Siberian Iris | Iris siberica
Silky Dogwood | Cornus amomum
Silver Birch | Betula pendula
Silver Falls Plant | Dichondra Argentea
Silver Maple | Acer saccharinum
Silver Mound | Artemisia schmidtiana 'silver mound'
Silver Squill | Ledebouria socialis
Skeleton Flower | Diphylleia grayi
Sky Plant | Tillandsia Ionantha
Skyrocket Juniper | Juniperus Scopulorum
Slipper Plant | Euphorbia lomelii
Smoke Tree | Cotinus coggygria
Smooth Hydrangea | Hydrangea arborescens
Snake Plant | Sansevieria trifasciata
Snap Pea | Pisum sativum
Snapdragon | Antirrhinum Majus
Snow Pea | Pisum sativum L.
Snow Queen Pothos | Epipremnum aureum 'Snow Queen'
Snow-In-Summer | Cerastium tomentosum
Snowball Bush Viburnum | Viburnum x carlcephalum
Snowdrop | Galanthus nivalis
Society Garlic | Tulbaghia violacea
Solomon's Seal | Polygonatum
Song Of India | Dracaena reflexa
Sourwood | Oxydendrum arboreum
Spaghetti Squash | Cucurbita pepo var
Spanish Bluebell | Hyacinthoides hispanica
Spanish Lavender | Lavendula stoechas
Spicebush | Lindera benzoin
Spider Lily | Lycoris
Spiderwort | Tradescantia
Spinach | Spinacia oleracea
Spineless Yucca | Yucca elephantipes
Spirea | Spiraea
Spotted Dead Nettles | Lamium maculatum
Spur Valerian | Centranthus ruber
Spurge Weed | Euphorbia maculata
St. Augustine Grass | Stenotaphrum secundatum
St. John's Wort | Hypericum perforatum
Staghorn Fern | Platycerium bifurcatum
Star Cactus | Astrophytum
Star of Bethlehem | Ornithogalum umbellatum
Starfish Cactus | Stapelia Hirsuta
Stargazer Lily | Lilium 'stargazer'
Stella d'Oro Daylily | Hemerocallis 'stella de oro'
Stephanotis | Marsdenia floribunda
Stewartstonian Azalea | Rhododendron 'stewartstonian'
Stinging Nettle | Urtica dioica
Stone Pine | Pinus pinea
Strawberry Indoors | Fragaria x ananassa
Strawberry Shake Philodendron | Philodendron erubescens ‘Strawberry Shake’
Strawberry Sundae Hydrangea | Hydrangea paniculata ‘Rensun’
Strawberry | Fragaria x ananassa
Strawflower | Xerochrysum bracteatum
String Bean | Phaseolus vulgaris
String Of Bananas | Senecio radicans
String Of Buttons | Crassula perforata
String Of Dolphins | Senecio peregrinus
String Of Hearts | Ceropegia woodii
String Of Pearls | Senecio rowleyanus
String of Rubies | Othonna capensis
String Of Turtles | Peperomia prostrata
Succulent Senecio | Senecio
Sugar Cane | Saccharum officinarum
Sugar Maple Tree | Acer saccharum
Sugar Tyme Crabapple | Malus 'sutyzam'
Sunburst Honey Locust | Gleditsia triacanthos var. inermis 'Suncole'
Sundew | Drosera capensis
Sunflower | Helianthus annuus
Sungold Tomato | Lycopersicon esculentum 'Sungold'
SunPatiens | Impatiens x hybrida
Swamp Hibiscus | Hibiscus Coccineus
Swamp Milkweed | Asclepias incarnata
Swamp White Oak | Quercus bicolor
Swedish Ivy | Plectranthus Verticillatus
Sweet Autumn Clematis | Clematis terniflora
Sweet Corn | Zea mays
Sweet Pea Flower | Lathyrus odoratus
Sweet Pea Shrub | Polygala dalmaisiana
Sweet Potato Vine | Ipomoea Batatas
Sweet Potato | Ipomoea Batatas
Sweet William | Dianthus barbatus
Sweet Woodruff | Galium odoratum
Sweetbay Magnolia | Magnolia virginiana
Swiss Cheese Plant | Monstera adansonii
Switchgrass | Panicum virgatum
Sycamore | Platanus occidentalis
Synogium Albo | Syngonium Podophyllum 'Albo Variegatum'
Tall Fescue Grass | Festuca arundinacea
Tamarack | Larix laricina
Tardiva Hydrangea | Hydrangea paniculata ‘Tardiva'
Tarragon | Artemisia dracunculus
Taylor Juniper | Juniperus virginiana 'Taylor'
Tea Olive | Osmanthus fragrans
Tea Plant | Camellia sinensis
Teddy Bear Cactus | Cylindropuntia Bigelovii
Teddy Bear Sunflower | Helianthus annuus 'Teddy Bear'
Texas Mountain Laurel | Dermatophyllum secundiflorum
Texas Star Hibiscus | Hibiscus Coccineus
Thai Basil | Ocimum basilicum var. thyrsiflora
Thai Pepper Plant | Capsicum annuum 'Bird's Eye'
Thanksgiving Cactus | Schlumbergera truncata
Thyme Indoors | Thymus vulgaris
Thyme | Thymus vulgaris
Ti Plant | Cordyline terminalis
Tiger Aloe | Gonialoe variegata
Tiger Jaws | Faucaria Tigrina
Tiger Lily | Lilium lancifolium
Toad Lily | Tricyrtis hirta
Tomatillo | Physalis philadelphica
Tomato | Solanum lycopersicum
Torch Ginger | Etlingera elatior
Totem Pole Cactus | Pachycereus schottii var. monstrosus
Tradescantia Nanouk | Tradescantia Fluminensis 'Nanouk'
Trailing Lantana | Lantana Montevidensis
Tree Hydrangea | Hydrangea paniculata
Tree Peony | Paeonia suffruticosa
Tree Philodendron | Philodendron bipinnatifidum
Tricolor Beech | Fagus sylvatica 'tricolor'
Triostar Stromanthe | Stromanthe sanguinea
Tropical Hibiscus | Hibiscus rosa-sinensis
Trumpet Vine | Campsis radicans
Tulip Tree | Liriodendron tulipifera
Tulips | Tulipa
Turmeric | Curcuma longa
Turtle Vine | Callisia Repens
Turtlehead | Chelone obliqua
Twinspur | Diascia
Utah Juniper | Juniperus osteosperma
Vanda Orchid | Vanda
Vanilla Strawberry Hydrangea | Hydrangea paniculata 'Renhy'
Vanilla | Vanilla plantifolia
Variegated String of Hearts | Ceropegia woodii var.
Venus Fly Trap | Dionaea muscipula
Verbena | Verbena x Hybrida
Veronica Spicata | Veronica spicata
Viburnum | Viburnum
Vinca Minor | Vinca minor
Vining Jasmine | Jasminum polyanthum
Violet | Viola
Virginia Bluebells | Mertensia virginica
Virginia Creeper | Parthenocissus quinquefolia
Virginia Sweetspire | Itea virginica
Wallflower | Erysimum
Wandflower | Gaura lindheimeri
Wasabi | Wasabia japonica
Washington Hawthorn | Crataegus phaenopyrum
Water Lettuce | Pistia stratiotes
Water Lily | Nymphaea
Watercress | Nasturtium officinale
Watermelon Peperomia | Peperomia argyreia
Watermelon | Citrullus lanatus
Wax Begonia | Begonia semperflorens
Weeping Cherry | Prunus subhirtella 'Pendula'
Weeping Fig | Ficus benjamina
Weeping Norway Spruce | Picea abies ‘Pendula’
Weeping Redbud | Cercis canadensis
Weeping Willows | Salix babylonica
Weigela | Weigela florida
Whale Fin Snake Plant | Dracaena masoniana
Wheat | Triticum aestivum
White Clover | Trifolium repens
White Egret Orchid | Habenaria radiata
White Feather Plantain Lily | Hosta 'White Feather'
White Fir | Abies concolor
White Oak | Quercus alba
White Spruce | Pilea Glauca
White Willow | Salix alba
White Wizard Philodendron | Philodendron erubescens 'White Wizard'
Wild Ginger | Asarum canadense
Wild Red Raspberry | Rubus idaeus
Wild Strawberry | Fragaria Virginiana
Winter Heath | Erica Carnea syn. Erica herbacea
Winter Jasmine | Jasminum nudiflorum
Winter Pansy | Viola hiemalis
Winterberry Holly | llex verticillata
Wintercreeper | Euonymus fortunei
Wishbone Flower | Torenia fournieri
Wisteria | Wisteria spp.
Witch Hazel | Hamamelis virginiana
Wood Grass | Sorghastrum nutans
Woodland Phlox | Phlox divaricata
Xanthosoma | Xanthosoma spp.
Yarrow | Achillea millefolium
Yaupon | Ilex vomitoria
Yellow Bells | Tecoma stans
Yellow Bird Magnolia | Magnolia x brooklynensis ‘Yellow Bird’
Yellow Iris | Iris pseudacorus
Yellow Pear Tomato | Solanum lycopersicum 'Yellow Pear'
Yerba Mate | Ilex paraguariensis
Yew Tree | Taxus
Yucca Plant | Yucca
Zebra Grass | Miscanthus sinensis 'zebrinus'
Zebra Plant | Aphelandra squarrosa
Zinnia | Zinnia elegans
Zoysia Grass | Zoysia spp.
ZZ Plant | Zamioculcas zamiifolia"""

mapping_lines = [line.strip() for line in mapping_text.splitlines() if line.strip()]
mapping_dict = {}
for line in mapping_lines:
    if ' | ' in line:
        common, species = line.split(' | ', 1)
        # Store lowercase to make matching easier
        mapping_dict[species.lower()] = common

csv_path = r'f:\Floracare\backend\scripts\plant_care_data_full.csv'

# Read the CSV
data = []
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    if 'common_name' not in fieldnames:
        fieldnames = ['common_name'] + fieldnames
    
    for row in reader:
        species_lower = row['species'].lower()
        if species_lower in mapping_dict:
            row['common_name'] = mapping_dict[species_lower]
        else:
            # Fallback to the species name if not in mapping, or just use capitalized species
            row['common_name'] = row['species'].title()
        data.append(row)

# Write the updated CSV
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"Updated CSV with {len(data)} rows.")

import psycopg2
from config import SUPABASE_URL, SUPABASE_KEY

# We should just use MCP apply_migration to add the column
