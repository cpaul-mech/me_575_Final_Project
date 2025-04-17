 portfolio_history, data, cash_history, stock_names
num_areas = len(stock_names) + 1
cmap = plt.get_cmap('tab20', num_areas)
colors = [cmap(i) for i in range(num_areas)]
plt.figure(figsize=(12, 6))
plt.stackplot(
    np.arange(stock_values.shape[0]),
    stack_data,
    labels=['Cash'] + stock_names,
    alpha=0.8,
    colors=colors
)
plt.xlabel('Days', fontsize=14)
plt.ylabel('Value ($)', fontsize=14)
plt.title('Portfolio Value Over Time', fontsize=16)
plt.legend(loc='upper left', ncol=2, fontsize=12)
plt.tight_layout()
plt.show()