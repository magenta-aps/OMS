# coding=UTF-8
"""
Created on April 30, 2016

@author: Sven Schlarb (https://github.com/shsdev), andreas
"""

import os.path
from pairtree import PairtreeStorageFactory, ObjectNotFoundException


def uri_to_safe_filename(uri):
    return uri.replace(":", "+")


class PairtreeStorage(object):
    """
    Pairtree storage class allowing to build a filesystem hierarchy for holding objects that are located by mapping identifier strings to object directory (or folder) paths with
    two characters at a time.
    """

    storage_factory = None
    repository_storage_dir = None

    def __init__(self, repository_storage_dir):
        """
        Constructor initialises pairtree repository

        @type       repository_storage_dir: string
        @param      repository_storage_dir: repository storage directory
        """
        self.storage_factory = PairtreeStorageFactory()
        self.repository_storage_dir = repository_storage_dir
        self.repo_storage_client = self.storage_factory.get_store(store_dir=self.repository_storage_dir, uri_base="http://")

    def identifier_object_exists(self, identifier):
        """
        Verify if an object of the given identifier exists in the repository

        @type       identifier: string
        @param      identifier: Identifier
        @rtype:     boolean
        @return:    True if the object exists, false otherwise
        """
        return self.repo_storage_client.exists(identifier, "data")

    def identifier_version_object_exists(self, identifier, version_num):
        """
        Verify if the given version of the object exists in the repository

        @type       identifier: string
        @param      identifier: Identifier
        type        version_num: int
        @param      version_num: version number
        @rtype:     boolean
        @return:    True if the object exists, false otherwise
        """
        version = '%05d' % version_num
        return self.repo_storage_client.exists(identifier, "data/%s" % version)


    def curr_version_num(self, identifier):
        """
        Get current version number

        @type       identifier: string
        @param      identifier: Identifier
        @rtype:     int
        @return:    Current version number
        """
        if not self.identifier_object_exists(identifier):
            raise ValueError("No repository object for id '%s'. Unable to get current version number." % identifier)
        version_num = 1
        while self.identifier_version_object_exists(identifier, version_num):
            version_num += 1
        version_num -= 1
        return version_num

    def get_object_path(self, identifier, version_num=0):
        """
        Get absolute file path of the stored object. If the version number is omitted, the path of the highest version
        number is returned.

        @type       identifier: string
        @param      identifier: Identifier
        @type       version_num: int
        @param      version_num: version number
        @rtype:     string
        @return:    Absolute file path of the stored object
        @raise      ObjectNotFoundException if the file is not available
        """
        if not self.identifier_object_exists(identifier):
            raise ValueError("No repository object for id '%s'. Unable to get requested version object path." % identifier)
        if version_num == 0:
            version_num = self.curr_version_num(identifier)
        if not self.identifier_version_object_exists(identifier, version_num):
            raise ValueError("Repository object '%s' has no version %d." % (identifier, version_num))
        version = '%05d' % version_num
        repo_obj = self.repo_storage_client.get_object(identifier, False)
        repo_obj_path = uri_to_safe_filename( os.path.join(repo_obj.id_to_dirpath(), "data/%s" % version))
        try:
            return next(os.path.join(repo_obj_path, f) for f in os.listdir(repo_obj_path) if os.path.isfile(os.path.join(repo_obj_path, f)))
        except StopIteration:
            raise ObjectNotFoundException("The file object does not exist in the repository")

