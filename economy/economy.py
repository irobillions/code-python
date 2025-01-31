def P_G_factor(i, n):
    i_float = i / 100
    terme_1 = pow((1 + i_float), n)
    terme_2 = (terme_1 - 1) / (i_float * terme_1)
    terme_3 = n / terme_1
    calc = terme_2 - terme_3

    p_g = (1 / i_float) * calc

    return p_g


print(P_G_factor(5, 5))
