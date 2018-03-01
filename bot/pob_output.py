from defusedxml import ElementTree
from discord import Embed
from marshmallow import Schema, fields, pprint

from models import Build, PlayerStat


def decode_build(build):
    """
    Decodes all build information and playerstats into the specific model we expect.
    :param build:
    :return:
    """
    build_info = Build(build.attrib['level'], build.attrib['targetVersion'], build.attrib['bandit'], build.attrib['className'],
                  build.attrib['ascendClassName'])
    for player_stat in build:
        build_info.appendStat(PlayerStat(player_stat.attrib['stat'],player_stat.attrib['value']))
    return build_info

def embed_message(obj):
    embed = Embed(title='PoB Discord', color=0x0433ff)
    embed.set_thumbnail(url='https: // docs.python.org / 2 / _static / py.png')
    embed.add_field(name='test', value='https: // docs.python.org / 2 / _static / py.png, inline = False')
    embed.add_field(name='test2', value='```dd```')
    return embed

def generate_output(pob_xml: ElementTree):
    build = pob_xml.find('Build')

    build=decode_build(build)
    ret = embed_message(build)
    # calcs=pob_xml.find('Calcs')
    # skills=pob_xml.find('Skills')
    # for item in pob_xml:
    #     print('{}'.format(item.attrib))
    #     for i in item:
    #         print('>> {}'.format(i.attrib))
    #         for j in i:
    #             print('>> >> {}'.format(j.attrib))

    return ret
