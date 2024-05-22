from encode_image import encode_image

map_images = {
    'Ascent': encode_image('static/maps/ascent_image.png'),
    'Bind': encode_image('static/maps/bind_image.png'),
    'Breeze': encode_image('static/maps/breeze_image.png'),
    'Icebox': encode_image('static/maps/icebox_image.png'),
    'Lotus': encode_image('static/maps/lotus_image.png'),
    'Split': encode_image('static/maps/split_image.png'),
    'Sunset': encode_image('static/maps/sunset_image.png'),
}


team_logos = {
    '100T': encode_image('static/logos/100t_logo.png'),
    'AG': encode_image('static/logos/ag_logo.png'),
    'BBL': encode_image('static/logos/bbl_logo.png'),
    'BILI': encode_image('static/logos/bili_logo.png'),
    'BLD': encode_image('static/logos/bleed_logo.png'),
    'C9': encode_image('static/logos/cloud9_logo.png'),
    'DFM': encode_image('static/logos/dfm_logo.png'),
    'DRG': encode_image('static/logos/drg_logo.png'),
    'DRX': encode_image('static/logos/drx_logo.png'),
    'EDG': encode_image('static/logos/edward_logo.png'),
    'EG': encode_image('static/logos/eg_logo.png'),
    'FNC': encode_image('static/logos/fnatic_logo.png'),
    'FPX': encode_image('static/logos/fpx_logo.png'),
    'FUR': encode_image('static/logos/furia_logo.png'),
    'FUT': encode_image('static/logos/fut_logo.png'),
    'G2': encode_image('static/logos/g2_logo.png'),
    'GENG': encode_image('static/logos/geng_logo.png'),
    'GX': encode_image('static/logos/giant_logo.png'),
    'GE': encode_image('static/logos/global_logo.png'),
    'TH': encode_image('static/logos/heretics_logo.png'),
    'JDG': encode_image('static/logos/jdg_logo.png'),
    'KC': encode_image('static/logos/karmine_logo.png'),
    'KOI': encode_image('static/logos/koi_logo.png'),
    'KRU': encode_image('static/logos/kru_logo.png'),
    'LEV': encode_image('static/logos/leviatan_logo.png'),
    'TL': encode_image('static/logos/liquid_logo.png'),
    'LOUD': encode_image('static/logos/loud_logo.png'),
    'GM8': encode_image('static/logos/mates_logo.png'),
    'MIBR': encode_image('static/logos/mibr_logo.png'),
    'NAVI': encode_image('static/logos/navi_logo.png'),
    'NOVA': encode_image('static/logos/nova_logo.png'),
    'NRG': encode_image('static/logos/nrg_logo.png'),
    'PRX': encode_image('static/logos/prx_logo.png'),
    'RRQ': encode_image('static/logos/rrq_logo.png'),
    'TS': encode_image('static/logos/secret_logo.png'),
    'SEN': encode_image('static/logos/sentinels_logo.png'),
    'T1': encode_image('static/logos/t1_logo.png'),
    'TLN': encode_image('static/logos/talon_logo.png'),
    'TEC': encode_image('static/logos/titan_logo.png'),
    'TRC': encode_image('static/logos/trace_logo.png'),
    'TYL': encode_image('static/logos/tyloo_logo.png'),
    'VIT': encode_image('static/logos/vitality_logo.png'),
    'WOL': encode_image('static/logos/wolves_logo.png'),
    'ZETA': encode_image('static/logos/zeta_logo.png'),
}
# Placeholder dictionary for full team names
team_full_names = {
    '100T': '100 Thieves',
    'AG': 'All Gamers',
    'BBL': 'BBL Esports',
    'BILI': 'Bilibili',
    'BLD': 'BLEED',
    'C9': 'Cloud9',
    'DFM': 'DetonatioN FocusMe',
    'DRG': 'Dragon Ranger Gaming',
    'DRX': 'DRX',
    'EDG': 'EDward Gaming',
    'EG': 'Evil Geniuses',
    'FNC': 'Fnatic',
    'FPX': 'FunPlus Phoenix',
    'FUR': 'Furia',
    'FUT': 'FUT Esports',
    'G2': 'G2 Esports',
    'GENG': 'Gen.G',
    'GX': 'GIANTX',
    'GE': 'Global Esports',
    'TH': 'Team Heretics',
    'JDG': 'JD Gaming',
    'KC': 'Karmine Corp',
    'KOI': 'KOI',
    'KRU': 'KRU Esports',
    'LEV': 'Leviatan',
    'TL': 'Team Liquid',
    'LOUD': 'LOUD',
    'GM8': 'Gentle Mates',
    'MIBR': 'MIBR',
    'NAVI': 'Natus Vincere',
    'NOVA': 'Nova Esports',
    'NRG': 'NRG Esports',
    'PRX': 'Paper Rex',
    'RRQ': 'Rex Regum Qeon',
    'TS': 'Team Secret',
    'SEN': 'Sentinels',
    'T1': 'T1',
    'TLN': 'Talon Esports',
    'TEC': 'Titan Esports Club',
    'TRC': 'Trace Esports',
    'TYL': 'TYLOO',
    'VIT': 'Vitality',
    'WOL': 'Wolves Esports',
    'ZETA': 'ZETA DIVISION',
}

regions_teams = {
    'Americas': ['100T', 'C9', 'EG', 'FUR', 'G2', 'KRU', 'LEV', 'LOUD', 'MIBR', 'NRG', 'SEN'],  # Add all teams in Americas
    'EMEA': ['BBL', 'FNC', 'FUT', 'GX', 'TH', 'KC', 'KOI', 'TL', 'GM8', 'NAVI', 'VIT'],  # Add all teams in EMEA
    'Pacific': ['BLD', 'DFM', 'DRX', 'GENG', 'GE', 'PRX', 'RRQ', 'TS', 'T1', 'TLN', 'ZETA'],  # Add all teams in Pacific
    'China': ['AG', 'BILI', 'DRG', 'EDG', 'FPX', 'JDG', 'NOVA', 'TEC', 'TRC', 'TYL', 'WOL'],  # Add all teams in China
    'VCT': ['100T', 'C9', 'EG', 'FUR', 'G2', 'KRU', 'LEV', 'LOUD', 'MIBR', 'NRG', 'SEN', 'BBL', 'FNC', 'FUT', 'GX', 'TH', 'KC', 'KOI', 'TL', 'GM8', 'NAVI', 'VIT', 'BLD', 'DFM', 'DRX', 'GENG', 'GE', 'PRX', 'RRQ', 'TS', 'T1', 'TLN', 'ZETA', 'AG', 'BILI', 'DRG', 'EDG', 'FPX', 'JDG', 'NOVA', 'TEC', 'TRC', 'TYL', 'WOL'],  # All teams
}

team_colors = {
    'Sentinels': '#d00434',
    'Cloud9': '#28ace4',
    'G2 Esports': '#040404',
    'KRU Esports': '#ff1c8c',
    'NRG Esports': '#080404',
    'Leviatan': '#70acdc',
    'LOUD': '#18fc04',
    '100 Thieves': '#ea3232',
    'MIBR': '#08040c',
    'Furia': '#040404',
    'Evil Geniuses': '#101424',
    'Karmine Corp': '#080404',
    'Fnatic': '#ff5c04',
    'Vitality': '#fffc04',
    'Team Liquid': '#001538',
    'BBL Esports': '#c39109',
    'Team Heretics': '#d5a938',
    'Natus Vincere': '#ffec04',
    'KOI': '#d2ae74',
    'FUT Esports': '#121824',
    'Gentle Mates': '#383838',
    'GIANTX': '#14141c',
    'EDward Gaming': '#020202',
    'Dragon Ranger Gaming': '#76f35d',
    'Bilibili': '#36d0f4',
    'Nova Esports': '#a854bc',
    'Wolves Esports': '#faa61a',
    'FunPlus Phoenix': '#ff0404',
    'Trace Esports': '#3f446a',
    'Titan Esports Club': '#e02c1c',
    'JD Gaming': '#d0142c',
    'All Gamers': '#da251c',
    'TYLOO': '#d63831',
    'Gen.G': '#ac8c04',
    'Global Esports': '#124091',
    'T1': '#e8042c',
    'Team Secret': '#080404',
    'BLEED': '#c3252d',
    'DetonatioN FocusMe': '#2364ec',
    'DRX': '#0f03a3',
    'Paper Rex': 'purple',
    'Rex Regum Qeon': '#f3aa36',
    'Talon Esports': '#e80444',
    'ZETA DIVISION': '#080404'
}


team_shapes = {
    'Sentinels': 'diamond',
    'Cloud9': 'circle',
    'G2 Esports': 'cross',
    'KRU Esports': 'square',
    'NRG Esports': 'square',
    'Leviatan': 'triangle',
    'LOUD': 'triangle-right',
    '100 Thieves': 'circle',
    'MIBR': 'triangle',
    'Furia': 'diamond',
    'Evil Geniuses': 'circle',
    'Karmine Corp': 'triangle',
    'Fnatic': 'square',
    'Vitality': 'triangle',
    'Team Liquid': 'square',
    'BBL Esports': 'triangle',
    'Team Heretics': 'cross',
    'Natus Vincere': 'square',
    'KOI': 'diamond',
    'FUT Esports': 'square',
    'Gentle Mates': 'circle',
    'GIANTX': 'diamond',
    'EDward Gaming': 'circle',
    'Dragon Ranger Gaming': 'triangle',
    'Bilibili': 'square',
    'Nova Esports': 'triangle',
    'Wolves Esports': 'square',
    'FunPlus Phoenix': 'circle',
    'Trace Esports': 'triangle',
    'Titan Esports Club': 'square',
    'JD Gaming': 'cross',
    'All Gamers': 'square',
    'TYLOO': 'diamond',
    'Gen.G': 'diamond',
    'Global Esports': 'cross',
    'T1': 'triangle',
    'Team Secret': 'circle',
    'BLEED': 'square',
    'DetonatioN FocusMe': 'triangle',
    'DRX': 'diamond',
    'Paper Rex': 'cross',
    'Rex Regum Qeon': 'triangle',
    'Talon Esports': 'circle',
    'ZETA DIVISION': 'square'
}
