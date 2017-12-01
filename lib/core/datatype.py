#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
重新封装dict类，使得可以直接通过dict.key访问key的内容
移植来源------sqlmap


TrieNode、Trie
"""

import copy
import types

class AttribDict(dict):


    def __init__(self, indict=None, attribute=None):
        if indict is None:
            indict = {}

        # Set any attributes here - before initialisation
        # these remain as normal attributes
        self.attribute = attribute
        dict.__init__(self, indict)
        self.__initialised = True

        # After initialisation, setting attributes
        # is the same as setting an item

    def __getattr__(self, item):
        """
        Maps values to attributes
        Only called if there *is NOT* an attribute with this name
        """

        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError("unable to access item '%s'" % item)

    def __setattr__(self, item, value):
        """
        Maps attributes to values
        Only if we are initialised
        """

        # This test allows attributes to be set in the __init__ method
        if "_AttribDict__initialised" not in self.__dict__:
            return dict.__setattr__(self, item, value)

        # Any normal attributes are handled normally
        elif item in self.__dict__:
            dict.__setattr__(self, item, value)

        else:
            self.__setitem__(item, value)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict

    def __deepcopy__(self, memo):
        retVal = self.__class__()
        memo[id(self)] = retVal

        for attr in dir(self):
            if not attr.startswith('_'):
                value = getattr(self, attr)
                if not isinstance(value, (types.BuiltinFunctionType, types.FunctionType, types.MethodType)):
                    setattr(retVal, attr, copy.deepcopy(value, memo))

        for key, value in self.items():
            retVal.__setitem__(key, copy.deepcopy(value, memo))

        return retVal





class Trie(object):

    def __init__(self,pathdict={}):
        self.root = pathdict
        self.type=""
        self.url=""
        self._404 = ""

    def insert(self, pathlist):
        """
        Inserts a word into the trie.
        :type pathlist: list
        :rtype: void
        """
        node = self.root
        for letter in pathlist:
            child = node.get(letter)
            if not child:
                node[letter] = {}
            node = node[letter]

    def starts_with(self, prefix):
        """
        Returns if there is any word in the trie
        that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        node = self.root
        node = node.get(prefix)
        if not node:
            return False
        return True

    def getPath(self,prefix="",not404=False):
        from urlparse import urljoin
        from lib.core.common import getResponse
        from lib.core.common import getRequest
        from lib.core.settings import headers
        from urlparse import urlparse
        import time
        """
        Returns words started with prefix
        :param prefix:
        :return: words (list)
        """
        def path404(url):
            if urlparse(url).path=="":
                return True
            req = getRequest(url, headers=headers)
            resp=getResponse(req)
            if resp.code==404:
                return False
            if self._404=="":
                req404 = getRequest(urlparse(url).scheme + "://" + urlparse(url).netloc + "/2b6b17d9173a182a4f86e8fa7877d4fb",headers=headers)
                self._404=getResponse(req404)
            if self._404.code==404:
                self._404="404$)$("
                return True
            else:
                self._404=self._404.read()
            try:
                if resp.read()!=self._404:
                    return True
            except:
                return False
        def _get_key(pre, pre_node):
            words_list = []
            if not pre_node :
                words_list.append(pre)
            for x in pre_node.keys():
                temp=pre +"/"+ str(x)
                if not not404 or path404(urljoin(self.url, temp)): #'''or temp.find(".js") != -1 or temp.find(".css") != -1 or temp.find(".txt") != -1 '''
                    if pre_node.get(x):
                        words_list.extend(_get_key(temp, pre_node.get(x)))
                    else:
                        words_list.extend(_get_key(pre +" "+ str(x), pre_node.get(x)))
            return words_list
        words = []
        node = self.root
        if prefix!="":
            if not self.starts_with(prefix):
                return words
            node = node.get(prefix)
        _list=_get_key(prefix, node)
        return _list






