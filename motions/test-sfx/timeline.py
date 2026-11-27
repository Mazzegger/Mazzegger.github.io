"""Source unique de vérité : instants des événements visuels (s) et SFX associés."""
W, H, FPS, DUR = 1080, 1920, 30, 13.2

T = dict(
    logo=1.00,                      # pop du logo
    letters=[1.40, 1.50, 1.60],     # atterrissage des lettres S, F, X
    typing=1.90,                    # début de frappe "MOTION × UCS"
    glitch=2.55,                    # transition glitch (fin ~2.95)
    panel_land=3.10,                # le panneau UI arrive
    hover=3.45, click=3.70,         # curseur sur le toggle, clic
    items=[3.95, 4.15, 4.35],       # 3 lignes qui apparaissent
    notif_land=4.85,                # bannière de notification posée
    load_start=5.30, load_end=6.45, # barre de chargement
    check=6.50,                     # coche de succès
    panel_out=7.30,                 # le panneau s'envole (pic du whoosh)
    count_start=7.45, count_end=8.90,
    hit=9.60,                       # gros impact "275 SONS"
    chips=[10.25, 10.45],           # pastilles qui arrivent
    sparkle=11.10,
    outro_logo=12.00,
    fade_out=12.70,
)

D = 'DESIGNED/'; U = 'USER INTERFACE/'; SW = 'SWOOSHES/'; C = 'CARTOON/'; M = 'MAGIC/'
# (fichier, instant, mode de synchro, gain dB, options)
#   start : début du fichier sur l'instant   hit : transitoire principal sur l'instant
#   peak  : pic d'énergie sur l'instant      end : fin du fichier sur l'instant
CUES = [
    (D + 'DSGNDron_Drone Ethereal Loop_MotionSynth_MotionLib.wav', 0.0, 'start', -24, dict(loop_to=DUR, fade_in=0.6, fade_out=0.9)),
    (D + 'DSGNStngr_Logo Reveal Corporate_MotionSynth_MotionLib.wav', T['logo'], 'hit', -2, {}),
    *[(SW + 'SWSH_Swish Tiny_MotionSynth_MotionLib.wav', t, 'peak', -9, {}) for t in T['letters']],
    (U + 'UIData_Text Typing Screen_MotionSynth_MotionLib.wav', T['typing'], 'start', -12, dict(cut=0.70)),
    (D + 'DSGNMorph_Glitch Transition_MotionSynth_MotionLib.wav', T['glitch'], 'start', -6, dict(cut=0.45)),
    (U + 'UIMvmt_Slide In Soft_MotionSynth_MotionLib.wav', T['panel_land'], 'peak', -8, {}),
    (U + 'UIClick_Hover Soft_MotionSynth_MotionLib.wav', T['hover'], 'start', -16, {}),
    (U + 'UIClick_Click Hard_MotionSynth_MotionLib.wav', T['click'], 'start', -8, {}),
    (U + 'UIClick_Toggle On_MotionSynth_MotionLib.wav', T['click'] + 0.02, 'start', -9, {}),
    *[(U + 'UIMvmt_Pop Appear_MotionSynth_MotionLib.wav', t, 'start', -9 - 1.5 * i, {}) for i, t in enumerate(T['items'])],
    (U + 'UIMvmt_Card Swipe Short_SurajET_SurajSFX06.wav', T['notif_land'] - 0.05, 'peak', -10, {}),
    (U + 'UIAlert_Chime Stair Up_SurajET_SurajSFX06.wav', T['notif_land'], 'start', -9, {}),
    (U + 'UIData_Data Chatter_MotionSynth_MotionLib.wav', T['load_start'], 'start', -15, dict(cut=T['load_end'] - T['load_start'])),
    (U + 'UIAlert_Success Arpeggio_MotionSynth_MotionLib.wav', T['check'], 'start', -6, {}),
    (SW + 'WHSH_Air Whoosh Medium_MotionSynth_MotionLib.wav', T['panel_out'], 'peak', -6, {}),
    (U + 'UIData_Score Counter Rollup_MotionSynth_MotionLib.wav', T['count_start'], 'start', -9, {}),
    (D + 'DSGNRise_Noise Riser 2s_MotionSynth_MotionLib.wav', T['hit'], 'end', -9, {}),
    (D + 'DSGNImpt_Cinematic Hit Big_MotionSynth_MotionLib.wav', T['hit'], 'hit', -1, {}),
    (D + 'DSGNBass_Sub Drop 2s_MotionSynth_MotionLib.wav', T['hit'], 'start', -5, {}),
    (D + 'DSGNBram_Braam Stab Short_MotionSynth_MotionLib.wav', T['hit'], 'start', -11, {}),
    *[(D + 'DSGNWhsh_Fast Pass By_MotionSynth_MotionLib.wav', t, 'peak', -8, {}) for t in T['chips']],
    (M + 'MAGShim_Magic Sparkle_MotionSynth_MotionLib.wav', T['sparkle'], 'start', -13, {}),
    (D + 'DSGNStngr_Logo Reveal Minimal_MotionSynth_MotionLib.wav', T['outro_logo'], 'start', -4, {}),
]
