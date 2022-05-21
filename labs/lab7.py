# NO ADDITIONAL IMPORTS!
import doctest
from text_tokenize import tokenize_sentences

characters = tuple([chr(i) for i in range(97,123)])

class Trie:
    """
    >>> t = Trie(str)
    >>> t['bat'] = 7
    >>> t['bar'] = 3
    >>> t['bark'] = ':)'
    >>> t['bark']
    ':)'
    >>> t['bar'] += 1
    >>> t['bar']
    4
    >>> list(t)
    [('bat', 7), ('bar', 4), ('bark', ':)')]
    >>> del t['bar']
    >>> t['bark']
    ':)'
    >>> 'bark' in t
    True
    >>> 'bar' in t
    False
    """
    def __init__(self, key_type):
        self.key_type = key_type
        self.value = None
        self.children = {}

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.
        """
        if type(key) is not self.key_type: 
            raise TypeError('not the right key_type')

        edge = self._key_element_to_edge(key[0])

        if len(key) == 1:
            if edge in self.children:
                t = self.children[edge]
                t.value = value
            else:
                t = Trie(self.key_type)
                t.value = value
                self.children.setdefault(edge, t)
        else:
            if edge in self.children:
                t = self.children[edge]
            else:
                t = Trie(self.key_type)
                self.children.setdefault(edge, t)
            t.__setitem__(key[1:], value)

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if type(key) is not self.key_type: 
            raise TypeError('not the right key_type')
        
        edge = self._key_element_to_edge(key[0])

        if edge not in self.children:
            raise KeyError('key not in trie')

        if len(key) == 1:
            if self.children[edge].value == None: 
                raise KeyError('no value associated with the key')
            return self.children[edge].value

        t = self.children[edge]
        return t.__getitem__(key[1:])

    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists. If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if len(key) == 0:
            raise KeyError('no key')
        if type(key) is not self.key_type: 
            raise TypeError('not the right key_type')

        edge = self._key_element_to_edge(key[0])

        child_trie = self.children[edge]

        if len(key) == 1:
            if child_trie.value == None:
                raise KeyError('no associated value')
            if child_trie.children == {}:
                del self.children[edge]
            else:
                child_trie.value = None
        else:
            child_trie.__delitem__(key[1:])
            if child_trie.children == {} and child_trie.value == None:
                del self.children[edge]

    def __contains__(self, key):
        """
        Is key a key in the trie? return True or False.
        """
        if type(key) is not self.key_type: 
            return False
            # raise TypeError('not the right key_type')

        if len(key) == 0:
            return False
        
        edge = self._key_element_to_edge(key[0])

        if edge not in self.children:
            return False

        if len(key) == 1:
            if self.children[edge].value == None: 
                return False
            return True

        t = self.children[edge]
        return t.__contains__(key[1:])

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator!
        """
        if self.children == {}: return   ## stopIteration

        for edge in self.children:
            child_trie = self.children[edge]
            if child_trie.value != None:   ## base case
                yield (edge, child_trie.value)
            for sub_edges, value in child_trie:   ## recursion
                yield (edge + sub_edges, value)

    ## Helper Function
    def _key_element_to_edge(self, key_element):
        if self.key_type == str:
            return self.key_type(key_element)
        elif self.key_type == tuple:
            return self.key_type([key_element])
        else:
            raise NotImplementedError('key_type not implemented')

    # ## Helper Function
    # def __combine(self, edge, sub_edges=None):
    #     if self.key_type == str:   ## key: a string
    #         if sub_edges == None:
    #             return edge
    #         else:
    #             return edge + sub_edges
    #     elif self.key_type == tuple:   ## key: a tuple
    #         if type(edge) == str:   ## key: a tuple of strings
    #             if sub_edges == None:
    #                 return (edge,)
    #             else:
    #                 return (edge,) + sub_edges
    #         else:
    #             raise NotImplementedError('key_type not implemented')
    #     else:
    #         raise NotImplementedError('key_type not implemented')


def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text

    >>> t = make_word_trie("bat bat bark bar")
    >>> t['bar']
    1
    >>> t['bat']
    2
    """
    t = Trie(str)

    for sentence in tokenize_sentences(text):
        for word in sentence.split(' '):
            if word in t:
                t[word] += 1
            else:
                t[word] = 1
    return t


def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    
    >>> text = "Hi there! How are you? Hi there!"
    >>> t = make_phrase_trie(text)
    >>> t[('hi', 'there')]
    2
    >>> list(t)
    [(('hi', 'there'), 2), (('how', 'are', 'you'), 1)]
    """
    t = Trie(tuple)

    for sentence in tokenize_sentences(text):
        key = tuple(sentence.split(' '))
        if key in t:
            t[key] += 1
        else:
            t[key] = 1
    return t


def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.

    >>> t = make_word_trie("bat bat bark bar")
    >>> autocomplete(t, "ba", 1)
    ['bat']
    >>> autocomplete(t, "ba", 2)
    ['bat', 'bar']
    >>> autocomplete(t, "bar", 2)
    ['bar', 'bark']
    >>> autocomplete(t, "be", 2)
    []

    >>> text = "Hi there! How are you? Hi there!"
    >>> t = make_phrase_trie(text)
    >>> autocomplete(t, ('hi',))
    [('hi', 'there')]
    """
    ## Specific cases
    if type(prefix) != trie.key_type:
        raise TypeError('prefix wrong type')
    if max_count == 0:
        return []

    ## Find node of the prefix
    t = trie
    for i in prefix:
        edge = t._key_element_to_edge(i)
        if edge in t.children:
            t = t.children[edge]
        else:
            return []

    result = []
    if prefix in trie:
        result.append((prefix, trie[prefix]))
    for key, value in t:   ## find potential suffix
        result.append((prefix + key, value))
    result.sort(key = lambda x: x[1], reverse = True)

    if not max_count or max_count > len(result):
        max_count = len(result)
    return [result[i][0] for i in range(max_count)]


def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.

    >>> t = make_word_trie("bat bat bark bar")
    >>> autocorrect(t, "bar", 3)
    ['bar', 'bark', 'bat']
    """
    ## Specific cases
    if type(prefix) != str or trie.key_type != str:
        raise TypeError('only for trie of words')
    if max_count == 0:
        return []

    result_complete = autocomplete(trie, prefix, max_count)

    if max_count and len(result_complete) == max_count:
        return result_complete

    result_edit = valid_edit(trie, prefix)

    if max_count: 
        max_count_edit = max_count - len(result_complete)
    if not max_count or max_count_edit > len(result_edit):
        max_count_edit = len(result_edit)
    return result_complete + [result_edit[i][0] for i in range(max_count_edit)]

## Helper Function
def valid_edit(trie, prefix):
    """
    >>> t = make_word_trie("bat bat bark bar")
    >>> valid_edit(t, 'bar')
    [('bat', 2)]
    >>> t = make_word_trie("dmon man mon")
    >>> valid_edit(t, 'mon')
    [('dmon', 1), ('man', 1)]
    """

    if type(prefix) != str or trie.key_type != str:
        raise TypeError('only for trie of words')
    
    result_edit = set()
    ## single-character insertion
    for i in range(len(prefix)):
        for character in characters:
            new_word = prefix[0:i] + character + prefix[i:]
            if new_word in trie:
                result_edit.add((new_word, trie[new_word]))
    ## single-character deletion
    for i in range(len(prefix)):
        new_word = prefix[0:i] + prefix[i+1:]
        if new_word in trie:
            result_edit.add((new_word, trie[new_word]))
    ## single-character replacement
    for i in range(len(prefix)):
        for character in characters:
            if character != prefix[i]:
                new_word = prefix[0:i] + character + prefix[i+1:]
                if new_word in trie:
                    result_edit.add((new_word, trie[new_word]))
    ## two-character transpose
    for i in range(len(prefix)-1):
        new_word = prefix[0:i] + prefix[i+1] + prefix[i] + prefix[i+2:]
        if new_word in trie:
            result_edit.add((new_word, trie[new_word]))
    
    result_edit = list(result_edit)
    result_edit.sort(key = lambda x: x[1], reverse = True)

    return result_edit

# @instrument
def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.

    >>> t = make_word_trie("bat bat bark bar")
    >>> word_filter(t, '*')
    [('bat', 2), ('bar', 1), ('bark', 1)]
    >>> word_filter(t, "???")
    [('bat', 2), ('bar', 1)]
    >>> word_filter(t, "*r*")
    [('bar', 1), ('bark', 1)]
    >>> word_filter(t, "****r")
    [('bar', 1)]
    """
    if len(pattern) == 0:
        return []
    
    result = []
    char = pattern[0]

    if len(pattern) == 1:
        if char in characters:
            if char in trie.children and trie.children[char].value != None:
                result.append((char, trie.children[char].value))
                return result
            else:
                return []
        if char == '?':
            for edge, t in trie.children.items():
                if t.value != None:
                    result.append((edge, t.value))
            return result
        if char == '*':
            result_set = set()
            if trie.value != None:
                result_set.add(('', trie.value))
            if trie.children != {}:
                for edge, t in trie.children.items():
                    for word, freq in word_filter(t, pattern):
                        result_set.add((edge + word, freq))
            return list(result_set)

    
    if char in characters:
        if char in trie.children:
            t = trie.children[char]
            for word, freq in word_filter(t, pattern[1:]):
                result.append((char + word, freq))
            return result
        else:
            return []
    if char == '?':
        for edge, t in trie.children.items():
            for word, freq in word_filter(t, pattern[1:]):
                result.append((edge + word, freq)) 
        return result
    if char == '*':
        if pattern[1] == '*':
            return word_filter(trie, pattern[1:])
        result_set = set()
        for word, freq in word_filter(trie, pattern[1:]):
            result_set.add((word, freq))
        for edge, t in trie.children.items():
            for word, freq in word_filter(t, pattern[1:]):
                result_set.add((edge + word, freq)) 
            for word, freq in word_filter(t, pattern):
                result_set.add((edge + word, freq))
        return list(result_set)
        


    # print('\n', 'pattern:', pattern, '\n')
    # result = []
    # i = 0
    # j = 0
    # for key, value in trie:
    #     if i % 10000 == 0:
    #         print('iter:', i)
    #     i += 1
    #     if is_pattern(key, pattern):
    #         print(j, ' word:', key)
    #         j += 1
    #         result.append((key, value))
    # return result

# ## Helper Function
# def is_pattern(character, pattern):
#     """
#     >>> is_pattern('bar', '*')
#     True
#     >>> is_pattern('bar', '*a*')
#     True
#     >>> is_pattern('bark', '*a*')
#     True
#     >>> is_pattern('bat', '???')
#     True
#     >>> is_pattern('bar', '*r*')
#     True
#     >>> is_pattern('bat', '??')
#     False
#     >>> is_pattern('boulder', '??')
#     False
#     >>> is_pattern('ba', '????')
#     False
#     """
#     if len(pattern) == 0:   ## base case 1
#         return False
#     if len(pattern) == 1:
#         if pattern[0] == '*':
#             return True
#     if len(character) == 1:   ## base case 2
#         useful_pattern = ''
#         for i in pattern:
#             if i != '*':
#                 useful_pattern += i
#         if len(useful_pattern) == 0:
#             return True
#         elif len(useful_pattern) == 1:
#             if useful_pattern[0] in ['?', character[0]]:
#                 return True
#             else:
#                 return False
#         else:
#             return False

#     ## recursion
#     if pattern[0] in characters:
#         if character[0] != pattern[0]:
#             return False
#         else:
#             return is_pattern(character[1:], pattern[1:])
#     if pattern[0] == '?':
#         return is_pattern(character[1:], pattern[1:])
#     if pattern[0] == '*':
#         if pattern[1] == '*':
#             pattern = pattern[1:]
#             return is_pattern(character, pattern)
#         elif pattern[1] == '?':
#             pattern = pattern[1] + pattern[0] + pattern[2:]
#             return is_pattern(character, pattern)
#         else:
#             if character[0] == pattern[1]:
#                 return is_pattern(character, pattern[1:])
#             else:
#                 return is_pattern(character[1:], pattern)
            

# you can include test cases of your own in the block below.
if __name__ == '__main__':
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
    # doctest.run_docstring_examples(word_filter, globals(), optionflags=_doctest_flags, verbose=False)

    # print(is_pattern('bar', '*r*'))
    # trie = Trie(tuple)
    # trie[(1, 2, 3)] = 'kitten'
    # trie[(1, 2, 0)] = 'tricycle'
    # trie[(1, 2, 0, 1)] = 'rug'
    # print(trie[(1, 2, 3)])

    # t = make_word_trie("bat bat bark bar")
    # word_filter(t, "***r")

    pass