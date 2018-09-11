from keras.layers import LSTM, Dense, Bidirectional, Masking
from keras.layers import Dropout, Concatenate, Flatten
from keras.layers import Permute, Subtract, Multiply, Dot, Lambda

import keras.backend as K


seq_len = 30


def rnn_siam_plain(embed_input1, embed_input2):
    ra = LSTM(300, activation='tanh')
    da1 = Dense(100, activation='relu')
    da2 = Dense(1, activation='sigmoid')
    x = Masking()(embed_input1)
    x = ra(x)
    y = Masking()(embed_input2)
    y = ra(y)
    diff = Lambda(lambda a: K.abs(a))(Subtract()([x, y]))
    prod = Multiply()([x, y])
    z = Concatenate()([x, y, diff, prod])
    z = Dropout(0.5)(z)
    z = da1(z)
    z = Dropout(0.5)(z)
    return da2(z)


def rnn_siam_stack(embed_input1, embed_input2):
    ra1 = LSTM(300, activation='tanh', return_sequences=True)
    ra2 = LSTM(300, activation='tanh')
    da1 = Dense(100, activation='relu')
    da2 = Dense(1, activation='sigmoid')
    x = Masking()(embed_input1)
    x = ra1(x)
    x = ra2(x)
    y = Masking()(embed_input2)
    y = ra1(y)
    y = ra2(y)
    diff = Lambda(lambda a: K.abs(a))(Subtract()([x, y]))
    prod = Multiply()([x, y])
    z = Concatenate()([x, y, diff, prod])
    z = Dropout(0.5)(z)
    z = da1(z)
    z = Dropout(0.5)(z)
    return da2(z)


def rnn_siam_bi(embed_input1, embed_input2):
    ra = LSTM(300, activation='tanh')
    ba = Bidirectional(ra, merge_mode='concat')
    da1 = Dense(100, activation='relu')
    da2 = Dense(1, activation='sigmoid')
    x = Masking()(embed_input1)
    x = ba(x)
    y = Masking()(embed_input2)
    y = ba(y)
    diff = Lambda(lambda a: K.abs(a))(Subtract()([x, y]))
    prod = Multiply()([x, y])
    z = Concatenate()([x, y, diff, prod])
    z = Dropout(0.5)(z)
    z = da1(z)
    z = Dropout(0.5)(z)
    return da2(z)


def attention(input, seq_len, reduce):
    x = Permute((2, 1))(input)
    x = Dense(seq_len, activation='softmax')(x)
    probs = Permute((2, 1))(x)
    output = Multiply()([input, probs])
    if reduce:
        output = Lambda(lambda a: K.mean(a, axis=1))(output)
    else:
        output = Flatten()(output)
    return output


def rnn_siam_attend(embed_input1, embed_input2):
    ra = LSTM(300, activation='tanh', return_sequences=True)
    da1 = Dense(100, activation='relu')
    da2 = Dense(1, activation='sigmoid')
    x = Masking()(embed_input1)
    x = ra(x)
    x = attention(x, seq_len, reduce=True)
    y = Masking()(embed_input2)
    y = ra(y)
    y = attention(y, seq_len, reduce=True)
    diff = Lambda(lambda a: K.abs(a))(Subtract()([x, y]))
    prod = Multiply()([x, y])
    z = Concatenate()([x, y, diff, prod])
    z = Dropout(0.5)(z)
    z = da1(z)
    z = Dropout(0.5)(z)
    return da2(z)


def rnn_siam_bi_attend(embed_input1, embed_input2):
    ra = LSTM(300, activation='tanh', return_sequences=True)
    ba = Bidirectional(ra, merge_mode='concat')
    da1 = Dense(100, activation='relu')
    da2 = Dense(1, activation='sigmoid')
    x = Masking()(embed_input1)
    x = ba(x)
    x = attention(x, seq_len, reduce=True)
    y = Masking()(embed_input2)
    y = ba(y)
    y = attention(y, seq_len, reduce=True)
    diff = Lambda(lambda a: K.abs(a))(Subtract()([x, y]))
    prod = Multiply()([x, y])
    z = Concatenate()([x, y, diff, prod])
    z = Dropout(0.5)(z)
    z = da1(z)
    z = Dropout(0.5)(z)
    return da2(z)


def rnn_join_plain(embed_input1, embed_input2):
    ra = LSTM(50, activation='tanh')
    da = Dense(1, activation='sigmoid')
    dot_input = Dot(2)([embed_input1, embed_input2])
    x = Masking()(dot_input)
    x = ra(x)
    return da(x)


def rnn_join_stack(embed_input1, embed_input2):
    ra1 = LSTM(50, activation='tanh', return_sequences=True)
    ra2 = LSTM(50, activation='tanh')
    da = Dense(1, activation='sigmoid')
    dot_input = Dot(2)([embed_input1, embed_input2])
    x = Masking()(dot_input)
    x = ra1(x)
    x = ra2(x)
    return da(x)


def rnn_join_bi(embed_input1, embed_input2):
    ra = LSTM(50, activation='tanh')
    ba = Bidirectional(ra, merge_mode='concat')
    da = Dense(1, activation='sigmoid')
    dot_input = Dot(2)([embed_input1, embed_input2])
    x = Masking()(dot_input)
    x = ba(x)
    return da(x)
