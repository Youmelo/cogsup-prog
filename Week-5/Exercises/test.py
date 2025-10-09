from expyriment import design, control

# 1. 初始化实验
exp = design.Experiment(name="SaveTest")
control.initialize(exp)

# 2. 添加数据列名
exp.add_data_variable_names(["Test_Column"])

# 3. 启动
control.start(subject_id=99)

# 4. 添加一行数据
exp.data.add(["Success!"])
print("已经添加数据，准备结束...")

# 5. 结束 (这是保存文件的命令)
control.end("实验成功结束！")
