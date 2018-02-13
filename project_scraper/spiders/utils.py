import re


_nonalphanum_re = re.compile(r'\W+')


def to_fieldname(s):
    """ Cleanup string to use for JSON fieldname. """

    # Remove non-alphanum characters and replace space with _
    return _nonalphanum_re.sub('', s.replace(' ', '_')).lower()
