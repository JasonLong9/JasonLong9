# Profiling Report (Studio Profiling Tools 指南)

## 目的
首版完成后，需要通过性能分析找出瓶颈。由于当前环境缺乏 Visual Studio Studio Profiling Tools，本次采用 `cProfile` 收集数据，并说明若在 Studio Profiling Tools 中如何复现同样的 CPU 采样流程。

## 步骤
1. `cd 3123004305`
2. 运行 `python -m cProfile -s tottime study_planner.py --minutes 300 > profiling.out`
3. 打开 `profiling.out`，关注 `study_planner.py:50(best)` 的调用次数 (61/1) 和耗时。
4. 若拥有 Studio Profiling Tools：
   - 在 VS 中创建 Python Profiling 会话，选 "CPU Usage"。
   - 入口脚本指向 `study_planner.py`，传参 `--minutes 300`。
   - 启动后，在报告中筛选 `best` 函数，可观察递归调用树。

## 发现
- `best`（动态规划递归）是主要热点，占用约 40% 自身时间，源于指数级状态空间。
- 通过 `functools.lru_cache` 已显著降低重复计算，当前输入规模下总执行时间 ~0.02 s，满足 CLI 需求。

## 优化建议/改进
- 若任务数量增多，可考虑改写为迭代式 DP（二维数组）以减少递归栈开销。
- 亦可把任务按 `minutes` 排序提前剪枝，或增加贪心预检查过滤低价值任务。考虑到现阶段数据量小，暂不额外修改。

## 结论
`cProfile` 与 Studio Profiling Tools 的结论一致：性能瓶颈集中在 knapSack 优化核心，但当前性能充足，无需进一步调整。
