# cocos2d-resPackage
 整理cocos2d工程项目下的资源 plist文件解析 png统计。  

 统计res文件夹下的plist&&png文件和png文件。   

  example test.plist解析	  

  解析的plist中不包含路径
  _test={
    key1:"value1.png",
    key2:"value2.png"
  }
  
  pngWithNoPlist.js 中统计资源中的散图
  _GamePngNames={
    key1:"/res/value1.png"
  }
  
  pngWithPlist.js 中统计资源中有plist的png图 
    _GamePlistNames={
    key1:"/res/value1.plist"
  }
  
  统计出散图的个数
  统计出plist图的个数
