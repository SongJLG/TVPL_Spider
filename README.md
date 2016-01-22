[# TVPL_Spider]
爬虫
爬取一些电视台的节目单
开盘区间突破是较为常见的日内交易策略之一，以今日开盘价加减一定比例的昨日振幅，确定上下轨。日内突破上轨时平空做多，突破下轨时平多做空。
Dual Thrust在形式上和开盘区间突破策略类似。不同点主要体现在两方面：Dual Thrust在Range的设置上，引入前N日的四个价位，使得一定时期内的Range相对稳定。
可以适用于日间的趋势跟踪；Dual Thrust对于多头和空头的触发条件，考虑了非对称的幅度，做多和做空参考的Range可以选择不同的周期数，也可以通过参数K1和K2来确定。
当K1<K2时，多头相对容易被触发；当K1>K2时，空头相对容易被触发,当K1>K2时，空头相对容易被触发。
因此，在使用该策略时，一方面可以参考历史数据测试的最优参数，另一方面，则可以根据自己对后势的判断，或从其他大周期的技术指标入手，阶段性地动态调整K1和K2的值。
这里参考了SkyPark策略，基于此进行了修改，着急回家过年，没咋测试。这里引入前5天的价位，同时k1,k2都设为了0.8，同样止损的也使用了k1,k2。都可以在配置文件里修改。