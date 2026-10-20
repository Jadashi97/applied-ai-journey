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

#11 example of calculating yearly pay based on hourly rate and hours worked with a stipend, bonus, tax deduction, wedding contribution, retirement contribution, expense deduction, loan repayment, and divide the loan repayment 3 quarters to personal loans and to credit card
personal_loan_repayment = 0.75 * loan_repayment
credit_card_repayment = 0.25 * loan_repayment
total_yearly_pay_after_personal_loan = total_yearly_pay_after_loan - personal_loan_repayment
total_yearly_pay_after_credit_card = total_yearly_pay_after_loan - credit_card_repayment
print(f"personal_loan_repayment: ${personal_loan_repayment}")
print(f"credit_card_repayment: ${credit_card_repayment}")
print(f"total_yearly_pay_after_personal_loan: ${total_yearly_pay_after_personal_loan}")
print(f"total_yearly_pay_after_credit_card: ${total_yearly_pay_after_credit_card}") 

#12 example of sum of all loans divided by 4
total_loans = loan_repayment + personal_loan_repayment + credit_card_repayment
average_loan_payment = total_loans / 4
print(f"total_loans: ${total_loans}")
print(f"average_loan_payment: ${average_loan_payment}")

#13 example showing what is left after all deductions and loans
final_yearly_pay = total_yearly_pay_after_loan - total_loans
print(f"final_yearly_pay: ${final_yearly_pay}") 