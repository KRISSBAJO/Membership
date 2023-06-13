from cloudinary_storage.storage import MediaCloudinaryStorage, StaticHashedCloudinaryStorage

class CustomMediaCloudinaryStorage(MediaCloudinaryStorage):
    def _exists_with_etag(self, name, content):
        try:
            return super()._exists_with_etag(name, content)
        except KeyError:
            return False

class CustomStaticHashedCloudinaryStorage(StaticHashedCloudinaryStorage):
    def _exists_with_etag(self, name, content):
        try:
            return super()._exists_with_etag(name, content)
        except KeyError:
            return False
