# 配置

程序配置分为全局配置和局部配置, 当程序运行时会优先采用全局配置, 当在局部配置中无需要的数据时, 会自动采用全局配置中的数据.
全局配置位于程序目录下的`global_config.json`, 局部配置位于程序目录下的`config.json`

## 配置项

全局配置如下

```JSON
{
    "except": [
        ".data/*"
    ],
    "info_folder": "./file",
    "tag": "./tag.json",
    "encoding": "utf-8",
    "data_folder":".data"
}
```

- `except`: 需要排除的文件
- `data`: 文件信息目录, 默认为`./file`且处于数据目录下, 可为绝对路径
- `tag`: 标签文件, 默认为`./tag.json`且处于数据目录下, 可为绝对路径
- `encoding`: 文件编码, 默认为`utf-8`
- `data_folder`: 数据目录, 默认为`.data`, 处于源文件目录下, 只能在默认设置中配置
