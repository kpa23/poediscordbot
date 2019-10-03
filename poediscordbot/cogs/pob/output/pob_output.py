from discord import Embed
from instance import config

from poediscordbot.cogs.pob.output import general_output, skill_output, config_output, charges_output, offense_output
from poediscordbot.cogs.pob.poe_data import build_checker
from poediscordbot.cogs.pob.util.pob import pob_minions
from poediscordbot.pob_xml_parser.models.build import Build
from poediscordbot.pob_xml_parser.models.gem import Gem
from poediscordbot.pob_xml_parser.models.skill import Skill


def create_embed(author, level, ascendency_name, class_name, main_skill: Skill, is_support):
    """
    Create the basic embed we add information to
    :param author: of the parsed message - str
    :param level: of the poe_data
    :param ascendency_name: to display
    :param class_name: to display if no ascendency has been chosen
    :param main_skill: main skill to display
    :return (Embed): the created Embed with the options set.
    """
    embed = Embed(title='tmp', color=config.color)
    gem_name = "Undefined"
    if is_support:
        gem_name = "Support"
    elif main_skill:
        gem_name = fetch_displayed_skill(gem_name, main_skill)

    if ascendency_name or class_name:
        url = 'https://raw.github.com/poediscord/poediscordbot/master/resources/img/' + (
            ascendency_name if ascendency_name != "None" else class_name) + '.png'
        embed.set_thumbnail(url=url)
    class_display_name = class_name if ascendency_name.lower() == 'none' else ascendency_name
    embed.title = f"{gem_name} - {class_display_name} (Lvl: {level})"
    if author:
        displayed_name = None
        try:
            displayed_name = author.nick
        except AttributeError:
            pass
        if not displayed_name:
            displayed_name = author.name

        if displayed_name:
            embed.title += " by: " + displayed_name
    return embed


def fetch_displayed_skill(gem_name, main_skill):
    main_gem = main_skill.get_selected()
    if isinstance(main_gem, Gem):
        display_name = f'{main_gem.get_name()}'
        if display_name and main_gem.minion_skill and main_gem.selected_minion:
            monster_name = pob_minions.get_monster_name(main_gem.selected_minion)
            if monster_name:
                display_name += f' ({monster_name})'
        return display_name
    else:
        return gem_name


def generate_info_text(tree, pastebin_key, web_poe_token):
    info_text = ""
    if pastebin_key:
        info_text += f"[Pastebin](https://pastebin.com/{pastebin_key}) | "
    info_text += f"[Web Tree]({tree}) "
    if web_poe_token:
        info_text += f"| [{config.web_pob_text}](https://pob.party/share/{web_poe_token}) "
    if config.poe_technology_enabled:
        info_text += f"| [{config.poe_technology_text}](https://poe.technology/poebuddy/{pastebin_key})  "
    info_text += f"\nCreated in [Path of Building](https://github.com/Openarl/PathOfBuilding). "
    return info_text


def generate_response(author, build: Build, minified=False, pastebin_key=None, consts=None, web_poe_token=None):
    """
    Build an embed to respond to the user.
    :param consts: poe constants - skill info
    :param author: name of the person triggering the action
    :param build: poe_data to parse an embed from
    :param minified (bool): whether to get a minified version or the full one
    :return: Filled embed for discord
    """
    is_support = build_checker.is_support(build)

    embed = create_embed(author, build.level, build.ascendancy_name, build.class_name,
                         build.get_active_skill(), is_support)
    # add new fields
    general_str = general_output.get_defense_string(build)
    if general_str:
        embed.add_field(name="General", value=general_str, inline=minified)

    key, offense = offense_output.get_offense(build, consts)
    if offense:
        embed.add_field(name=key, value=offense,
                        inline=minified)

    charges_str = charges_output.get_charges(build)
    if charges_str:
        embed.add_field(name="Charges", value=charges_str, inline=minified)
    # if not minified, add detailed infos.
    if not minified:
        skill = skill_output.get_main_skill(build)
        if skill:
            embed.add_field(name="Main Skill", value=skill, inline=minified)
        conf_str = config_output.get_config_string(build.config)
        if conf_str:
            embed.add_field(name="Config", value=conf_str, inline=minified)
    # output
    embed.add_field(name='Info:', value=generate_info_text(build.tree, pastebin_key, web_poe_token))

    return embed
