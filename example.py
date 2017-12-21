from datasets import Datasets

ds = Datasets({"address": "http://localhost:5000"})
# ds = Datasets()
print(ds.address)

# print(ds.info("8b88a424-dbd8-4032-8be7-a930a415b9a5"))
# print(ds.paths("8b88a424-dbd8-4032-8be7-a930a415b9a5"))
# print(ds.create({"name": "aaa", "from": "8b88a424-dbd8-4032-8be7-a930a415b9a5", "tags": ["a"]}, path=""))
# print(ds.create({"name": "aaa", "from": "8b88a424-dbd8-4032-8be7-a930a415b9a5", "tags": ["a"]}))
