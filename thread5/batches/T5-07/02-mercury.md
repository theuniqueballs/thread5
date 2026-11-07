# T5-07 — 02 MERCURY: карточки слотов (компакт)

Сеанс: MERCURY (2026-10-29). Стык L1 проверен: HEAT объявлена, 24 истории
с полями SOL, cast-заявки учтены, EXP-оверлей переопределён автором
(кандидаты ОС соло-слотами), бриф обновлён.

Каст 11/21: R25 Slime (P07) · R31 Flower (P08) · R22 Flame-salamander
(P09) · R13 Merfolk (P12) · R32 Golem (P13) · R21 Mushroom (P15) · R40
Medusa (P16) · R33 Ghost (P18) · R35 Arachne (P20) · R19 Cecaelia (P21) ·
R11 Bat (P22). Люди: P04, P05, P06, P10, P11, P17, P19, P23, P24. ОС —
свой канон (P01 Sue human, P02 Yui human-fangs, P03 Ila goat-kin). RF ≤2
у каждой, адаптация гардероба обязательна (прорези хвоста/крыльев/рог),
collision_table чист (Sue/Yui/Ila-подписи никому не выданы).

Регистры (формой тела, без тега возраста): student P06/P10/P14/P15/P19/P22
· young P04/P05/P07/P08/P12/P18/P20/P21 · milf-form P09/P11/P13/P16/P17/
P23/P24. ОС — канон body_type VERBATIM (Sue FAM-B B3 slender; Yui FAM-B
B3-B4 soft feminine; Ila athletic stone-kin FAM-B B3-B4).

| Слот | Кин | Тело | Волосы/глаза | Палитра | Гардероб/покрытие | Канал | Stack (4 группы) |
|---|---|---|---|---|---|---|---|
| P01 | — (canon) | slender, narrow frame, FAM-B B3 | platinum twin ponytails / soft purple (right), eyepatch LEFT | P15_INDUSTRIAL_STEEL | GAR16 transparent latex plugsuit, ports spine | wet-sheer (латекс-глянец) | W21,B10,E03,M08 |
| P02 | — (canon fangs) | soft feminine, FAM-B B3-B4 | yellowish-blonde pink tips / golden ringed | P80_SALT_APPETITE | ring-cut swimsuit + gold beads | swim_wet (dresser; single-source) | W07,B12,E21,S12 |
| P03 | — (goat horns+ears) | athletic stone-kin, strong thighs, FAM-B B3-B4 | silver-white waves / mist-white | P79_WAX_NOON | borrowed thin tee (nobody's) | wet-sheer | W07?→W32,B11,U04,I17 |
| P04 | — | light wiry, FAM-C B2 | honey-copper / amber | P64_SUNRISE_INDIGO | work overall + tee, sleeves tied | — (PG-13) | W19,B11,M05,D28 |
| P05 | — | soft slim, FAM-B B3 | dark blonde braid / brown | P118_FIRST_FLOOR_LILAC | GAR21 pinafore + blouse | — (PG-13) | W16,B10,E14,M03 |
| P06 | — | lean dancer, FAM-C B2 | coal-black braids / grey | P119_METRO_NAP_BRASS | GAR08 satin skirt + GAR12 harness | r-geometry | W31,B12,A04,D07 |
| P07 | R25 | gel silhouette, semi-liquid FAM-B B3 | translucent seaform / pale teal | P90_FAIRY_LAUNDRY | GAR05 wet linen shirt | r-geometry | W07,B22,E08,I17 |
| P08 | R31 | blooming soft, FAM-B B4 | dark rose / honey | P93_GLASS_BELL_JAR | GAR33 apron over thin shift; strap_migrated (GAR48) | — (R) | W05?→W08,B06,E01,S24 |
| P09 | R22 | ripe warm, FAM-A B5 | copper-ash / ember-amber | P60_FIRE_ASH | GAR19 damp dark bandage wrap | bumps (dresser №28) | W05,B01,S11,H09 |
| P10 | — | slim student, FAM-B B3 | ash blonde / green | P96_GRIMOIRE_AND_JAM | GAR26 tie-collar blouse + pencil skirt | pantyline-lower | W23,B09,C10,A14 |
| P11 | — | soft full, FAM-B B4 | chestnut-copper / brown | P102_CONFIDANT_BRASS | GAR32 organza blouse (thin) | contact-physics | W13,B17,M03,D05 |
| P12 | R13 | sleek swimmer, FAM-B B3 | sea-teal / sea-glass | P43_OCEAN_DEEP_PRISM | GAR01 soaked silk slip | wet-sheer-delivery | W07,B10,E01,S21 |
| P13 | R32 | heavy slow, FAM-A B5-B7 | clay-copper / warm gold | P31_VOID_ASH | GAR04 leather corset-apron, open back | — (R) | W15,B08,S11,M18 |
| P14 | R35 | lithe weaver, FAM-C B2-B3 | raven / steel | P36_VOID_RUST | GAR20 robe slipped to waist + tape crosses | tape-only | W11?→tape,B01,U21,M08 |
| P15 | R21 | slight budding, FAM-C B2 | mushroom-beige / pale amber | P104_HUSH_GREEN | thin cotton shift (damp front) | r-geometry | W08,B10,S12,M05 |
| P16 | R40 | mature bloom, FAM-A B5 | emerald coils / pale lime | P23_VOID_VIOLET | GAR24 tulle petticoat sheer | r-geometry | W10,B10,L05,G03 |
| P17 | — | wide hips heavy soft bust, FAM-A B5-B7 | pepper-black streaked grey / dark | P92_WITCHING_HOUR_KITCHEN | apron bare-back (wet), nothing underneath | contact-physics | W07,B01,M03,S22 |
| P18 | R33 | taper lower, FAM-C B2 | frost-white / cold glow | P21_VOID_BLACK | GAR31 pajama shorts + nightgown top | r-geometry | W30,B24,I02,G14 |
| P19 | — | soft young athletic, FAM-B B3 | flax blonde / grey-blue | P32_VOID_ICE | GAR02 fine turtleneck, frozen | nipple-ridges | W30,B01,I22,H13 |
| P20 | R35 | lithe, small bust, FAM-C B2 | blue-black / opal glint | P55_SYMBIOTE_BIOLUM | GAR07 mesh top (waist), handbra | handbra-open-palms | W26?→mesh,B03,D23,I22 |
| P21 | R19 | soft streamlined, FAM-B B3-B4 | weed-dark / pearl | P83_MIDNIGHT_LAGOON | GAR14 soaked sarong | r-geometry | W08,B10,C13,I17 |
| P22 | R11 | light wiry, FAM-C B2 | charcoal-violet / phosphor-yellow | P27_VOID_STARLIGHT | thin tank, steam-soaked | wet-sheer-delivery | W07,B10,I17,H09 |
| P23 | — | full motherly, FAM-A B5-B7 | wheat / warm brown | P53_OPULENT_DECADENCE | boyshorts + dropped work shirt | — (R) | W13,C05,B13,A14 |
| P24 | — | ceremonial full, FAM-B B4 | dark honey / nacre | P06_OBSIDIAN_GOLD | dark thin shirt (warm-cling) | bumps (dresser №28) | W05,B01,H09,G14 |
| P25 | EXP R26 | wasp-waist firm, FAM-B B3 | amber-striped dark / honey-gold | P115_HONEY_TRAP | GAR22 dark silk wrap (honey-gloss) | bumps (dresser №28) | W05,B01,S11,H09 |
| P26 | EXP R23 | athletic shark-line, FAM-B B3-B4 | slate / black-ring white | P117_TIDEPOOL_TEAL | GAR34 clear vinyl rashguard (wet) | wet-sheer-delivery | W07,B10,S12,I17 |
| P27 | EXP R34 | full soft, FAM-A B5 | flame-red / ember | P35_VOID_EMBER | GAR06 dark robe, steam-damp | bumps (dresser №28) | W27,B01,S22,H09 |
| P28 | EXP R37 | curvy FAM-B B4 | wine-purple / garnet | P75_VELVET_GRAVITY | GAR38+GAR03+GAR09 underwear-as-outfit ☠ | underwear-as-outfit ☠ (1/2) | W03?→lace,B03,L03,G07 |
| P29 | EXP R41 | slim student, FAM-C B2 | black + silver streak / violet | P95_SPELLBOUND_LINEN | GAR30 pleated microskirt + blouse | — (R) | W26,B11,D26,G06 |
| P30 | EXP R39 | slender young, FAM-C B2 | pale gold / white-lit | P56_AURORA_BOREALIS_NIGHT | white shift, wings folded | — (PG-13) | W30?→shift,B10,L06,G14 |
| P31 | EXP R24 | broad-soft, FAM-A B5 | ash-lilac / wine | P49_CINNABAR_DREAM | GAR17 kimono slipped shoulder | — (R) | W16,E03,B06,S02 |
| P32 | EXP R36 | plush soft, FAM-B B3-B4 | warm brown / amber | P78_RUST_LULL | GAR28 knit shoved up | contact-physics | W13,B17,M03,I13 |
| P33 | EXP R30 | small sturdy, FAM-C B2 | moss-green / gold-rim | P123_BEACON_RED_RAIN | rain poncho, bare legs | — (PG-13) | W09,B10,S12,G04 |

Броски ULTIMATE DICE: перебросов не было — коллизий окна/burn/преткновений
не возникло (коды отобраны вне ЗАПРЕТА ОКНА и burn; выбор ручной по
вайб-фиту, как в T5-04/05R/06; записи в ultimate-dice.json не требуются).
Каналы-кандидаты ☠: 1/2 (P28). bumps — dresser-канал (№28), в
delivery-реестре не числится: 4 слота, помечено в заметке EARTH.
P02 swim_wet — single-source канал (receipt T4-31 P21 «золото»), честная
пометка: доказательная база тоньше wet-sheer.
