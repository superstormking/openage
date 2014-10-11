from ..convert.util import dbg
import os

contenttemplate = """\
{prefix} Warning: this file was auto-generated; manual changes are futile.
{prefix} For details, see buildsystem/codegen.cmake and py/openage/codegen.

{code}"""

def generate_all_raw(cpp_src_dir):
    # add invocations to all individual generators here.
    from ..convert import datafile
    for filename, content in datafile.generate_gamedata_structs(cpp_src_dir):
        yield "gamedata/%s" % filename, content

def generate_all(cpp_src_dir):
    for filename, content in generate_all_raw(cpp_src_dir):
        # test whether filename matches the pattern *.gen.*
        basename = os.path.basename(filename)
        try:
            # this will raise a ValueError if basename doesn't have exactly
            # three dot-separated components
            basename, marker, suffix = basename.split('.')

            # if the middle component isn't "gen", raise a ValueError
            # manually
            if not (basename and marker and suffix) or marker != 'gen':
                raise ValueError()
        except ValueError:
            dbg("error in codegen: required filename format is " +
                "[base].gen.[suffix], but filename is %s" % filename, 0)
            exit(1)

        # get absolute filename
        absfilename = "".join((cpp_src_dir, os.path.sep, filename))

        # post-process content
        extension = os.path.splitext(filename)[1].lower().strip()
        if extension in {'.h', '.hpp', '.c', '.cpp'}:
            comment_prefix = '//'
        else:
            comment_prefix = '#'

        content = contenttemplate.format(prefix=comment_prefix, code=content)

        yield absfilename, filename, content