#1 example of calculating weekly pay based on hourly rate and hours worked
hourly_rate = 90
hours = 40
weekly_pay = hourly_rate * hours
print(f"weekly_pay: ${weekly_pay}")

#2 example of calculating monthly pay based on hourly rate and hours worked
monthly_pay = weekly_pay * 4
print(f"monthly_pay: ${monthly_pay}")

#3 example of calculating yearly pay based on hourly rate and hours worked
yearly_pay = monthly_pay * 12
print(f"yearly_pay: ${yearly_pay}")

#4 example of calculating yearly pay based on hourly rate and hours worked with a stipend
stipend = 2500
total_yearly_pay = yearly_pay + stipend
print(f"total_yearly_pay: ${total_yearly_pay}")

#5 example of calculating yearly pay based on hourly rate and hours worked with a stipend and bonus
bonus = 5000
total_yearly_pay_with_bonus = total_yearly_pay + bonus
print(f"total_yearly_pay_with_bonus: ${total_yearly_pay_with_bonus}")

#6 example of calculating yearly pay based on hourly rate and hours worked with a stipend, bonus, and tax deduction
tax_deduction = 0.2 * total_yearly_pay_with_bonus
total_yearly_pay_after_tax = total_yearly_pay_with_bonus - tax_deduction
print(f"total_yearly_pay_after_tax: ${total_yearly_pay_after_tax}")

#7 example of calculating yearly pay based on hourly rate and hours worked with a stipend, bonus, tax deduction, and wedding contribution
wedding_contribution = 20000
total_yearly_pay_after_wedding = total_yearly_pay_after_tax - wedding_contribution
print(f"total_yearly_pay_after_wedding: ${total_yearly_pay_after_wedding}")

#8 example of calculating yearly pay based on hourly rate and hours worked with a stipend, bonus, tax deduction, wedding contribution, and retirement contribution
retirement_contribution = 0.25 * total_yearly_pay_after_wedding
total_yearly_pay_after_retirement = total_yearly_pay_after_wedding - retirement_contribution
print(f"retirement_contribution: ${retirement_contribution}")
print(f"total_yearly_pay_after_retirement: ${total_yearly_pay_after_retirement}")

#9 example of calculating yearly pay based on hourly rate and hours worked with a stipend, bonus, tax deduction, wedding contribution, retirement contribution, and expense deduction
expense_deduction = 0.8 * total_yearly_pay_after_retirement
total_yearly_pay_after_expenses = total_yearly_pay_after_retirement - expense_deduction
print(f"expense_deduction: ${expense_deduction}")
print(f"total_yearly_pay_after_expenses: ${total_yearly_pay_after_expenses}")

#10 example of calculating yearly pay based on hourly rate and hours worked with a stipend, bonus, tax deduction, wedding contribution, retirement contribution, expense deduction, and loan repayment
loan_repayment = 0.2 * total_yearly_pay_after_expenses
total_yearly_pay_after_loan = total_yearly_pay_after_expenses - loan_repayment
print(f"loan_repayment: ${loan_repayment}")
print(f"total_yearly_pay_after_loan: ${total_yearly_pay_after_loan}")